package simula.ciscojobscheduling;

import java.util.ArrayList;
import java.util.List;

import com.model.Job;
import com.model.Resource;

import simula.oclga.Problem;

public class Problem_scheduling implements Problem {

	int[][] values;

	public static boolean optimize = true;
	
	double timeBudget;
	int jobsMin; // testjob Min
	int jobsMax; // testjob Max
	List<Job> jobs;
	
	int jobNum = 0;
	
	public int getjobNum(){
		return jobNum;
	}
	public void setjobNum(int jobNum){
		this.jobNum = jobNum;
	}
	
	public int[][] getValues() {
		return values;
	}

	public void setValues(int[][] values) {
		this.values = values;
	}

	// timebudget
	public void settimeBudget(double timeBudget) {
		this.timeBudget = timeBudget;
	}

	public void setjobsMin(int jobsMin) {
		this.jobsMin = jobsMin;
	}

	public void setjobsMax(int jobsMax) {
		this.jobsMax = jobsMax;
	}

	public void setjobs(List<Job> jobs) {
		this.jobs = jobs;
	}

	public int[][] getConstraints() {
		int valuesOfConstraints[][] = new int[1][3];
		valuesOfConstraints[0][0] = jobsMin;
		valuesOfConstraints[0][1] = jobsMax;
		valuesOfConstraints[0][2] = 0;
		setValues(valuesOfConstraints);
		return values;
	}

	@Override
	public double getFitness(int[] v) { //it would be better to retrun a list or String[], the first value is fitness function, the others are the jobid of selected test cases.
		double countJobs=0;
		double tm = 0; // fitness value
		int temptime = 0; //calculating the whole time for the solution
		for (int j = 0; j<v[0];j++){
			
				int jobId = (int)(Math.random() * ((jobsMax)-1) + 1);
				Job tempjob = jobs.get(jobId);
				int maxuploadcost = 0;
				int maxsubnetcost = 0;
				
				double sumweight = 0;
				ArrayList <Resource> tempresources = tempjob.getRequiredResource(); // associated test resources to a test case
				for (int i = 0; i<tempresources.size(); i ++){
					Resource tempresource = tempresources.get(i);
					if (tempresource!=null){
						if (maxuploadcost < tempresource.getUploadcost())
							maxuploadcost = tempresource.getUploadcost();
						if (maxsubnetcost < tempresource.getSubnetcost())
							maxsubnetcost = tempresource.getSubnetcost();
						sumweight = sumweight + tempresource.getWeight();
					}
				}
							
				// the whole time used for the solution
				temptime = temptime + tempjob.getMaxRunTime() + maxuploadcost + maxsubnetcost;
				//if it takes more time break out of the loop and return the fitness function with the total calculated jobs
				if (temptime>=timeBudget){
					temptime = temptime - tempjob.getMaxRunTime() - maxuploadcost - maxsubnetcost;
					continue;
				}else {
					countJobs++;
					double numNorm = 1- Nor(tempjob.getPriority());
					tm =tm +sumweight*(tempjob.getMaxRunTime() + maxuploadcost + maxsubnetcost)*numNorm;
					tm = Nor(tm);			
				}	
			}
		//find the job that is left and find it by dividing with total
		double jobb = jobsMax-countJobs;
		double jobNor = (double)jobb/jobsMax;
		tm = tm*0.1 + jobNor*0.9;
		//	System.out.println(countJobs);
			setjobNum ((int)countJobs);
		//	System.out.println("New starts \n");
			return tm;
	}
	
	// normalization function
	public double Nor(double n) {
		double m = n / (n + 1);
		return m;
	}
}
