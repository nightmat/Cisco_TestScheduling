package com.data;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import com.model.Job;
import com.model.Resource;

public class DataGenerator {

	public List<Job> jobs;
	public List<Resource> resources;
	public int[] tempArray;
	
	public DataGenerator(){		
		jobs = new ArrayList<Job>();
		resources = new ArrayList<Resource>();		
	}
	
	public void generateJobs(int numberRange, int min, int max){
		Job[] job = new Job[numberRange];
		int[] temp = new int[max];
		
		temp = generateNumbers(numberRange, min, max);
		
		for (int i=0; i< numberRange;i++){
			int time = randomWithRange(0, 100);
			
			job[i] = new Job();
			job[i].setJobId(temp[i]);
			job[i].setMaxRunTime(time);
			jobs.add(job[i]);
		}
		System.out.println("Done first one about jobs");
	}
		
	public void generateResources(int numberRange, int min, int max){
		Resource[] resource = new Resource[numberRange];
		int[] temp = new int[max];
		
		temp = generateNumbers(numberRange, min, max);
		
		double weightTemp = randomWithRange(0, 10);
		
		double weight = (double)weightTemp/numberRange; //Can be changed later
		
		for (int i=0; i< numberRange;i++){
			resource[i] = new Resource();
			resource[i].setResourceId(temp[i]);
			resource[i].setWeight(weight);
			resources.add(resource[i]);
		}

	}
	
	public void addResource(Job job, int maxResource){
		int minResource = 1;
		ArrayList<Resource> resource = new ArrayList<Resource>();
		
		int numberResource = randomWithRange(minResource,maxResource);
		int size = resources.size();
		int temp= 0;
		
		for (int j=0; j< numberResource; j++){			
			temp= randomWithRange(minResource,size-1);	
			resource.add(j, resources.get(temp));
		}
		job.setRequiredResource(resource);

	}
	
	public void setJobResource(int maxResource){
		int size= jobs.size();
		
		for (int i=0;i<size;i++){
			addResource(jobs.get(i), maxResource);
		}
		
	}
	
	public double getWeight(int value){
		int length = resources.size();		
		return (double)(tempArray[value])/length;
	}
		
	public int[] generateNumbers(int number, int min, int max){
		int[] temp = new int[max];
	
		List<Integer> numbers = new ArrayList<Integer>();
		
			
			for (int i=0;i<max;i++){
				int num = randomWithRange(min,max);
				numbers.add(num);		
			}
			Collections.shuffle(numbers);
		
			for (int j=0;j<number;j++){
				temp[j]=numbers.get(j);
			}
		
		
		return temp;
	}
	
	
	//Generate random number within a given range
	int randomWithRange(int min, int max)
	{
	   int range = (max - min) + 1;     
	   return (int)(Math.random() * range) + min;
	}
	
	
	public List<Job> getJobArray() {
		return jobs;
	}

	public void setJobArray(List<Job> jobArray) {
		this.jobs = jobArray;
	}
}
