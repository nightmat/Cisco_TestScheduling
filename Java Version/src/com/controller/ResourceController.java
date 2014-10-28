package com.controller;

import java.sql.ResultSet;
import java.sql.SQLException;

import com.model.Job;

public class ResourceController {
	public Job[] job;
	public int numberJobs;
		
	public DatabaseConnection databaseConnection;
	public ResultSet resultSet;
	public ResultSet countSet;
	public int length;
	public int[] tempArray;
	
	public ResourceController(){
		length =0;
		tempArray = new int[1000]; //maximum should be the max value of the resource id
		databaseConnection = new DatabaseConnection();
	}
	
	//Get resources
	public void queryResource(){		
		String selectJob= "SELECT id FROM public.resource order by id";
		String countItems= "SELECT COUNT(*) FROM public.resource";
		
			databaseConnection.connect();
			resultSet = databaseConnection.queryTable(selectJob);
			countSet = databaseConnection.queryTable(countItems);
			try{
				while (countSet.next()) 
					length = countSet.getInt("count");
			}catch(SQLException e) {			 
				System.out.println(e.getMessage());
			}
						
			try{
				while (resultSet.next()) 
					tempArray[resultSet.getInt("id")]++;						
			}catch(SQLException e) {			 
				System.out.println(e.getMessage());
	 
			}
				
		databaseConnection.disconnect();	
		
	}
	
	public double getWeight(int value){
		return (double)(tempArray[value])/length;
	}
	
	
}
