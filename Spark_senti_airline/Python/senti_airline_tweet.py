import os
import sys

if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME']='/opt/apache-spark/spark-3.1.1-bin-hadoop2.7'
SPARK_HOME=os.environ['SPARK_HOME']
print(SPARK_HOME)

if 'PYTHONPATH' not in os.environ:
    os.environ['PYTHONPATH']='/opt/anaconda3/bin/python3.6'
PYTHONPATH=os.environ['PYTHONPATH']

sys.path.insert(0,os.path.join(SPARK_HOME,"python"))
sys.path.insert(0,os.path.join(SPARK_HOME,"python","lib"))
sys.path.insert(0,os.path.join(SPARK_HOME,"python","lib","pyspark.zip"))
sys.path.insert(0,os.path.join(SPARK_HOME,"python","lib","py4j-0.10.9-src.zip"))

###Import modules and create spark session

#import modules
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
#-----------------------------------------------------------
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover



#create Spark session
appName = "Sentiment Analysis in Spark"
spark = SparkSession \
    .builder \
    .appName(appName) \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

###Read data file into Spark dataFrame

#read csv file into dataFrame with automatically inferred schema
tweets_csv_B = spark.read.csv('/home/vijani/NetBeansProjects/Spark_senti_airline/Python/Tweets_airline2.csv', inferSchema=True, header=True)
tweets_csv_B.show(truncate=False, n=3)
tweets_csv = tweets_csv_B.filter(col("airline_sentiment").isNotNull()).select("text", "airline_sentiment")
###Select the related data

#select only "text" and "airline_sentiment" column, 

data = tweets_csv.select("text", "airline_sentiment")
data.show(truncate = False,n=5)

data1 = data.withColumn("airline_sentiment", regexp_replace(data["airline_sentiment"], "positive", "1"))
data3 = data1.withColumn("airline_sentiment", regexp_replace(data1["airline_sentiment"], "negative", "0"))
#data3 = data2.withColumn("airline_sentiment", regexp_replace(data2["airline_sentiment"], "neutral", "-1"))

data3.show(truncate = False,n=5)

#and cast "airline_sentiment" column data into integer
data_n = data3.select(col("text").alias("SentimentText"), col("airline_sentiment").cast("Int").alias("label"))
data_n.show(truncate = False,n=5)

data_new = data_n.filter(col("SentimentText").isNotNull()).select("SentimentText", "label")

###Divide data into training and testing data

#divide data, 70% for training, 30% for testing
dividedData = data_new.randomSplit([0.7, 0.3]) 
trainingData = dividedData[0] #index 0 = data training
testingData = dividedData[1] #index 1 = data testing
train_rows = trainingData.count()
test_rows = testingData.count()
print ("Training data rows:", train_rows, "; Testing data rows:", test_rows)

###Prepare training data

###Separate "SentimentText" into individual words using tokenizer

tokenizer = Tokenizer(inputCol="SentimentText", outputCol="SentimentWords")
tokenizedTrain = tokenizer.transform(trainingData)
print(tokenizedTrain)
tokenizedTrain.printSchema()
tokenizedTrain.show(truncate=False, n=5)  ## ---------------------> gives an error

###Removing stop words (unimportant words to be features)

swr = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="MeaningfulWords")
SwRemovedTrain = swr.transform(tokenizedTrain)
SwRemovedTrain.show(truncate=False, n=5)  ## ---------------------> gives an error

###Converting words feature into numerical feature. In Spark 2.2.1,it is implemented in HashingTF funtion using Austin Appleby's MurmurHash 3 algorithm

hashTF = HashingTF(inputCol=swr.getOutputCol(), outputCol="features")
numericTrainData = hashTF.transform(SwRemovedTrain).select('label', 'MeaningfulWords', 'features')
numericTrainData.show(truncate=False, n=3)  ## ---------------------> gives an error


###Train our classifier model using training data

lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10, regParam=0.01)
model = lr.fit(numericTrainData)  ## ---------------------> gives an error
print ("Training is done!")

###Prepare testing data

tokenizedTest = tokenizer.transform(testingData)
SwRemovedTest = swr.transform(tokenizedTest)
numericTest = hashTF.transform(SwRemovedTest).select('Label', 'MeaningfulWords', 'features')
numericTest.show(truncate=False, n=2)

###Predict testing data and calculate the accuracy model


prediction = model.transform(numericTest)
predictionFinal = prediction.select("MeaningfulWords", "prediction", "Label")
predictionFinal.show(n=4, truncate = False)
correctPrediction = predictionFinal.filter(predictionFinal['prediction'] == predictionFinal['Label']).count()
totalData = predictionFinal.count()
print("correct prediction:", correctPrediction, ", total data:", totalData, ", accuracy:", correctPrediction/totalData)

###Returning value to frontend
if len(sys.argv) > 1:
    comment = sys.argv[1]
    comment = comment.replace("_"," ")
    print("testing for input:");
    print(comment)
    r = spark.createDataFrame([(comment,0)],['SentimentText', 'label'])
    tokenizedTest = tokenizer.transform(r)
    SwRemovedTest = swr.transform(tokenizedTest)
    numericTest = hashTF.transform(SwRemovedTest).select('Label', 'MeaningfulWords', 'features')
    numericTest.show(truncate=False, n=2)

    prediction = model.transform(numericTest)
    predictionFinal = prediction.select("MeaningfulWords", "prediction", "Label")
    predictionFinal.show(n=4, truncate = False)
    result = predictionFinal.select("prediction").first()[0]
    print(result)
    if result == 1.0:
        sys.exit(21)
    else:
        sys.exit(20)




