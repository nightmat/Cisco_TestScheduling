package com.model;

import java.util.ArrayList;
import java.util.List;

public class Job {
	private int jobId;
	private int maxRunTime;
	private int taskId;
	public List<Integer> list = new ArrayList<Integer>();
	private int size;
	public ArrayList<Resource> requiredresource = new ArrayList<Resource>();
	private int priority;
	
	public Job(){
		this.priority = (int )(Math.random() * 10 + 1); ;
	}
	
	public int getJobId() {
		return jobId;
	}
	public void setJobId(int jobId) {
		this.jobId = jobId;
	}
	public int getMaxRunTime() {
		return maxRunTime;
	}
	public void setMaxRunTime(int maxRunTime) {
		this.maxRunTime = maxRunTime;
	}
	public int getTaskId() {
		return taskId;
	}
	public void setTaskId(int taskId) {
		this.taskId = taskId;
	}
	public List<Integer> getList() {
		return list;
	}
	public int getSize() {
		return size;
	}
	public void setSize(int size) {
		this.size = size;
	}
	public int getPriority() {
		return priority;
	}
	public void setPriority(int priority) {
		this.priority = priority;
	}
	public ArrayList<Resource> getRequiredResource() {
		return requiredresource;
	}
	public void setRequiredResource(ArrayList<Resource> requiredresource) {
		this.requiredresource = requiredresource;
	}
	
	
}
