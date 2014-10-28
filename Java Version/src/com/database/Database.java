package com.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Database {
	private String url;
	private String portNumber;
	private String dbName;
	private String userName;
	private String passWord;
    public Connection myConnection;

	public void setUrl(String url) {
		this.url = url;
	}

	public void setDbName(String dbName) {
		this.dbName = dbName;
	}

	public void setUserName(String userName) {
		this.userName = userName;
	}

	public void setPortNumber(String portNumber) {
		this.portNumber = portNumber;
	}

	public void setPassWord(String passWord) {
		this.passWord = passWord;
	}
	
	public Database(){
		myConnection = null;
	}
    
    
   public Connection getConnection() {
        try {
        	Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
        	 
			System.out.println("Where is your PostgreSQL JDBC Driver? "
					+ "Include in your library path!");
			e.printStackTrace();
			return myConnection;
 
		}
 
		System.out.println("PostgreSQL JDBC Driver Registered!");
 
		try {
			myConnection= DriverManager.getConnection( "jdbc:postgresql://"+ url + ":" + portNumber + "/" + dbName, userName , passWord);
        }catch (SQLException e) {
 
			System.out.println("Connection Failed! Check output console");
			e.printStackTrace();
			return myConnection;
 
		}
		if (myConnection != null) {
			System.out.println("You are connected to the database now");
		} else {
			System.out.println("Connection failed");
		}
		return myConnection;
    }

    public Connection conn(){
        return this.myConnection;
    }
    
    
    public void closeConnection(){
        try{
            myConnection.close();
        } catch (SQLException e){
            System.out.println("SQL Exception: ");
            e.printStackTrace();
        }

    }
    
}