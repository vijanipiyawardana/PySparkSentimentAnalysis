<%-- 
    Document   : index
    Created on : Jun 19, 2021, 10:38:11 PM
    Author     : vijani
--%>

<%@page import="java.util.ArrayList"%>
<%@page import="com.vijani.Comment"%>
<%@page import="java.util.List"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>FlightPlanner</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">

        <style>
            .content {
                max-width: 1000px;
                margin: auto;
            }
            div.c {
                text-align: right;
            } 
        </style>
    </head>
    <body>

        <div class="content"><br>
            <h1>Airmate Flight Planner International</h1><br>
            <img src ="images/plane1.png"/>
            <table>
                <tr>
                    <td></td> 
                </tr>

            </table>
        </div>
        <%
            String successMsg = (String)request.getAttribute("success");
            if(successMsg == null) {
                successMsg = "true";
            }
            if (successMsg == "false") {
                    
                
        %>
        <div class="alert alert-warning" role="alert">
  You message is under review
</div>
        <%
            }
        %>
        <div class="container mt-5">
            <div class="row d-flex justify-content-center">
                <div class="col-md-8">
                    <div class="headings d-flex justify-content-between align-items-center mb-3">
                        <h6>Reviews</h6>

                    </div>
                    <div class="card p-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="user d-flex flex-row align-items-center"> <img src="images/user.png" width="30" class="user-img rounded-circle mr-2"> <span><small class="font-weight-bold text-primary">james_olesenn</small> <small class="font-weight-bold">@JetBlue credit to you for replying.  I???ll look forward to hopefully one of those 103 on my flight home tonight :)</small></span> </div> <small>2 days ago</small>
                        </div>

                    </div>
                    <div class="card p-3 mt-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="user d-flex flex-row align-items-center"> <img src="images/user.png" width="30" class="user-img rounded-circle mr-2"> <span><small class="font-weight-bold text-primary">olan_sams</small> <small class="font-weight-bold">@USAirways KUDOS to your phone support and Charlotte gate staff!</small></span> </div> <small>3 days ago</small>
                        </div>

                    </div>
                    <div class="card p-3 mt-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="user d-flex flex-row align-items-center"> <img src="images/user.png" width="30" class="user-img rounded-circle mr-2"> <span><small class="font-weight-bold text-primary">rashida_jones</small> <small class="font-weight-bold">@JetBlue Thank you guys! Brilliant customer service</small></span> </div> <small>3 days ago</small>
                        </div>

                    </div>


                    <%                        
                        List<Comment> comments = (List<Comment>) request.getAttribute("comments");
                        if (comments == null) {
                            comments = new ArrayList<Comment>();
                        }
                        for (Comment c : comments) {
                    %>
                    <div class="card p-3 mt-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="user d-flex flex-row align-items-center"> <img src="images/user.png" width="30" class="user-img rounded-circle mr-2"> <span><small class="font-weight-bold text-primary"><%=c.getName()%></small> 

                                    <small class="font-weight-bold"><%=c.getComment()%> </small></span> </div> <small>now</small>
                        </div>

                    </div>
                    <%
                        }
                    %>

                </div>
                <div class="content">
                    <form action="CommentServlet" method="POST">
                        <div class="form-group">
                            <label for="nameInput">Name</label>
                            <input type="name" class="form-control" id="inputName" name = "inputName" placeholder="Enter your name here">
                        </div>
                        <div class="form-group">
                            <label for="commentInput">Comment</label>
                            <input type="comment" class="form-control" id="inputComment" name="inputComment" placeholder="Type your comment here">
                        </div><br>
                        <div class="c">
                            <button type="submit" class="btn btn-primary">Add Comment</button>
                    </form>
                </div></div>
        </div>
    </div
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script>

</body>
</html>
