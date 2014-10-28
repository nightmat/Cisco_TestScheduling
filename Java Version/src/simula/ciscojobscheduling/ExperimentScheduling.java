package simula.ciscojobscheduling;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;
import com.controller.JobController;
import com.controller.ResourceController;
import com.data.DataGenerator;
import com.model.Job;
import com.model.Resource;


import simula.oclga.Search;

public class ExperimentScheduling {

	/**
	 * @param args
	 */
	List<Job> jobs = new ArrayList<Job>();
	List<Resource> resources = new ArrayList<Resource>();
	int values[];
	DecimalFormat df = new DecimalFormat("0.000");  //number of decimal places you want for printing out the output
	static BufferedWriter file;
	static int timebudget = 4000; //time you have for running the jobs
	static int numberofjobs = 0;
	static int numberofresources = 0;
	static int jobsMin = 1;   //minimum jobs you want to execute
	static int jobsMax = 300; //maximum jobs you want to execute
	int loopNum = 50;   //number of output for different searches

	public JobController jobController;
	public ResourceController resourceController;

	private static File fileName;
	private static DataGenerator dataGenerator;

	public static void main(String[] args) throws Exception {
		fileName = new File("C:\\Personal\\practice\\files\\test.txt");   //output location

		// if file does not exists, then create it
		if (!fileName.exists()) {
			fileName.createNewFile();
		}

		ExperimentScheduling ex = new ExperimentScheduling();
		ex.initi();
		ex.getValues_1();
		file.close();
	}

	public void initi() {
		dataGenerator = new DataGenerator();
		dataGenerator.generateJobs(jobsMax, 1, 13000);    //random jobs created within the range from 1 to 13000
		dataGenerator.generateResources(300, 1, 900);	//300 random resources created from 1 to 900
		dataGenerator.setJobResource(5);		//Job linked to maximum 5 resource randomly
		jobs = dataGenerator.getJobArray();
	}

	public int[] getValues_1() throws Exception {
		FileWriter fw = new FileWriter(fileName.getAbsoluteFile());
		file = new BufferedWriter(fw);
		Search[] s = new Search[] { new simula.oclga.AVM(),
				new simula.oclga.SSGA(100, 0.75), new simula.oclga.OpOEA(),
				new simula.oclga.RandomSearch() };
		String[] s_name = new String[] { "AVM", "GA", "(1+1)EA", "RS" };

		for (int sea = 0; sea < 4; sea++) {
			long start = System.currentTimeMillis();
			for (int K = 0; K < loopNum; K++) {
				Problem_scheduling p = new Problem_scheduling();
				p.setjobs(jobs);
				p.settimeBudget(timebudget);
				p.setjobsMin(jobsMin);
				p.setjobsMax(jobsMax);
				s[sea].setMaxIterations(2000);
				Search.validateConstraints(p);
				int[] v_1 = s[sea].search(p);
				double m = p.getFitness(v_1);
				int n = p.getjobNum();
			//	file.write(df.format(m) + "\t"); //
				file.write(n + "\t"); //
				
			//	System.out.printf("%s %d has ended \n", s_name[sea], K);

			}
			long end = System.currentTimeMillis();
			System.out.println(s_name[sea]);
			System.out.println ((end-start)/loopNum);
			file.write("\r");
			file.flush();
		}
		return null;
	}
}
