/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.vijani;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 *
 * @author vijani
 */
public class CommentServlet extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        String name = request.getParameter("inputName");
        String comment = request.getParameter("inputComment");

        List<Comment> commentList;
        commentList = (List<Comment>) request.getAttribute("comments");

        if (commentList == null) {
            commentList = new ArrayList<>();

        }
        Boolean valid = false;

        try {
            valid = validateComment(comment);
        } catch (Exception e) {
            e.printStackTrace();
        }

        if (valid) {
            Comment commentObj = new Comment(name, comment);
            commentList.add(commentObj);
        } else {
            request.setAttribute("success", "false");
        }

        request.setAttribute("comments", commentList);
        request.getRequestDispatcher("index.jsp").forward(request, response);
    }

    private Boolean validateComment(String comment) throws Exception {
        comment = comment.replace("'", " ").replace("\"", " ");
        String command = "python3 /home/vijani/NetBeansProjects/Spark_senti_airline/Python/senti_airline_tweet.py "
                + "'" + comment.replace(" ", "_") + "'";
        System.out.println("=== " +command);
        String[] args = new String[]{
            
            
        };
        Process exec = Runtime.getRuntime().exec(command);
        long t1 = System.currentTimeMillis();
        
        

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(exec.getInputStream()));

        BufferedReader stdError = new BufferedReader(new InputStreamReader(exec.getErrorStream()));

// Read the output from the command
        System.out.println("Here is the standard output of the command:\n");
        String s = null;
        while ((s = stdInput.readLine()) != null) {
            System.out.println(s);
        }

// Read any errors from the attempted command
        System.out.println("Here is the standard error of the command (if any):\n");
        while ((s = stdError.readLine()) != null) {
            System.out.println(s);
        }
        
        int exitValue = exec.waitFor();
        long t2 = System.currentTimeMillis();
        long diff = t2 - t1;

        while (exec.isAlive()) {
            Thread.sleep(500);
            System.out.println("live");
        }
        exitValue = exec.exitValue();
System.out.println("exit value =====> " + exitValue + " run for " + diff);
        if (exitValue == 21) {
            return true;
        } else {
            return false;
        }
    }
    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
