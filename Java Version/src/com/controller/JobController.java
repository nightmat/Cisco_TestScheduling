package com.controller;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import com.model.Job;
import com.model.Resource;

public class JobController {
	public List<Job> jobArray = new ArrayList<Job>();

	public Job[] job;
	public int numberJobs;	
	public DatabaseConnection databaseConnection;
	public ResultSet resultSet;
	public static ResourceController resourceController;
	
	public JobController(){
		job = new Job[1500000];
		databaseConnection = new DatabaseConnection();
		resourceController = new ResourceController();
	}
	
	public void queryJob(){		
		String selectJob= "SELECT job.id, job.max_runtime,task_id FROM public.job order by job.max_runtime";
		int i=0;
			databaseConnection.connect();
			resultSet = databaseConnection.queryTable(selectJob);
			try{
				while (resultSet.next()) {
					job[i] = new Job();
					job[i].setJobId(resultSet.getInt("id"));
					job[i].setMaxRunTime(resultSet.getInt("max_runtime"));
					job[i].setTaskId(resultSet.getInt("task_id"));
					
					getJobArray().add(i,job[i]);
	
					i++;
				}
			}catch(SQLException e) {			 
				System.out.println(e.getMessage());
	 
			}
			
		numberJobs = getJobArray().size();
		databaseConnection.disconnect();	
		
	}
	
	//Get resource for the job
	public void queryResource(){	
		Resource[] resource = new Resource[6520000];
		ResultSet resultResource;
		databaseConnection.connect();
		System.out.println("Query resource has started");	
		
		resourceController.queryResource();
		
		for (int i=0; i<2001; i++){

			String selectReqResource = "SELECT resource_required.id FROM public.resource_required where resource_required.task_id = " + getJobArray().get(i).getTaskId();
			
			resultSet = databaseConnection.queryTable(selectReqResource);
			int j=0;
			resource[i] = new Resource();
			try{
				while (resultSet.next()) {
					job[i].list.add(j,resultSet.getInt("id"));
									
					int a = job[i].list.get(j);
					String number = String.valueOf(a);
					int length = number.length();
					char[] digits = number.toCharArray();
					if (length==6){
						String selectResource = "SELECT id FROM public.resource where resource.id = " + digits[3]+digits[4]+digits[5];
						if (selectReqResource!=null){
							resultResource = databaseConnection.queryTable(selectResource);
							while(resultResource.next()) {
								resource[i].setResourceId(resultResource.getInt("id"));
								resource[i].setWeight(resourceController.getWeight(resource[i].getResourceId()));

								job[i].requiredresource.add(j,resource[i]);
							}
						}
					} else
						job[i].requiredresource.add(j,null);
				
				}
			}catch(SQLException e) {			 
					System.out.println(e.getMessage());		 
			}			
			job[i].setSize(job[i].list.size());
			
		}
		System.out.println("done");
	
		databaseConnection.disconnect();	
		
	}

	public List<Job> getJobArray() {
		return jobArray;
	}

	public void setJobArray(List<Job> jobArray) {
		this.jobArray = jobArray;
	}
	
}
