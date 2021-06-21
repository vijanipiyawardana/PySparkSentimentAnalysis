/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.vijani;

/**
 *
 * @author vijani
 */
public class Comment {

    public Comment(String name, String comment) {
        this.name = name;
        this.comment = comment;
    }
    
    String name;
    String comment;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }
    
    
    
}
