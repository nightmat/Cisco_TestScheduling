package com.model;

public class Resource {
	
	public int resourceid;
	public double weight; // (the number of available resouces in the pool/the whole number)
	public boolean currentbuild;
	public int uploadcost;
	public int subnetcost; // cost for subnet
	
	public Resource()  {
		//simulation for uploadcost
		subnetcost = (int)Math.random()*10; //from 0 to 100 (integer)
		
		// simulation for uploadcost
		if (Math.random() < 0.5) {
			this.currentbuild = true;
			uploadcost = 1;
		}
		else {
			this.currentbuild = false;
			if (Math.random()<0.8)
				uploadcost = 4;
			else uploadcost = 6; // if there are "snooy or ex20" in the hostname for Resource table
		}
	}
	
	public int getResourceId() {
		return resourceid;
	}

	public void setResourceId(int resourceid) {
		this.resourceid = resourceid;
	}

	public double getWeight() {
		return weight;
	}

	public void setWeight(double weight) {
		this.weight = weight;
	}

	public int getUploadcost() {
		return uploadcost;
	}

	public void setUploadcost(int uploadcost) {
		this.uploadcost = uploadcost;
	}

	public int getSubnetcost() {
		return subnetcost;
	}

	public void setSubnetcost(int subnetcost) {
		this.subnetcost = subnetcost;
	}
		
}
