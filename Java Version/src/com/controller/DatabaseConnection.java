package com.controller;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import com.database.Database;

public class DatabaseConnection {	

	private Database database;
	public Connection myConnection;
	public Statement statement;
	public ResultSet rs;
	public boolean connection;
	
	//Set your database credentials here
	public DatabaseConnection(){
		database = new Database();
		
		database.setUrl("127.0.0.1");
		database.setPortNumber("5432");
		database.setDbName("Cisco");
		database.setUserName("postgres");
		database.setPassWord("dipesh");
		connection = false;		
	}
	
	
	public void connect(){
		myConnection = database.getConnection();
		if (myConnection !=null)
			connection = true;
	}
	
	public void disconnect(){
		database.closeConnection();
		connection = false;
	}
	
	//For querying the database
	public ResultSet queryTable(String tableSQL){		
			try{
				Statement statement = myConnection.createStatement();
				statement.setFetchSize(100000);
				rs = statement.executeQuery(tableSQL);
			}catch(SQLException e) {			 
				System.out.println(e.getMessage());
	 
			}	
		return rs;
	}
	
}
