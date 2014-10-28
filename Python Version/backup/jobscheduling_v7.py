__author__ = 'Ruihua and Shuai'

import random
import string
import time
import copy
import math
import sys


#the main programme0
def main():
    print "start"

    jobs = []
    resources = []

   

    ex = CiscoJobSchedulingExecute(jobs=jobs, resources=resources,
                                   jobsMin=1, jobsMax=len(jobs), loopNum=10)
    ex.getValues_1()


#The main class for scheduling:
class CiscoJobSchedulingExecute():
    def __init__(self, jobs=[], resources=[], jobsMin=0, jobsMax=0, loopNum=10, fileName="result.txt"):
        self.jobs = jobs  #test cases
        self.resources = resources  #test resources
        self.values = []
        self.jobsMin = jobsMin
        self.jobsMax = jobsMax
        self.loopNum = loopNum
        self.fileName = fileName


    def getValues_1(self, MaxIterations=500):
        file_w = open(self.fileName, 'w')
        s = [OpOEA()]
        # s_name = ["(1+1)EA"]

        for sea in range(len(s)):
            for k in range(self.loopNum):
                p = Problem_scheduling()
                p.setresources(self.resources)
                p.setjobs(self.jobs)
                p.setjobsMin(self.jobsMin)
                p.setjobsMax(self.jobsMax)
                s[sea].setMaxIterations(MaxIterations)
                t = Search()
                t.validateConstraints(p)
                v_1 = s[sea].search(p)
                # p is an instance of Problem_scheduling,
                # and search(p) will use the function getSolution in Problem_scheduling.

                optimal_test_order = p.getFitness(v_1)

                # We use it below to print result in file.
                for ii in range(len(optimal_test_order)):
                    if ii == 0:
                        file_w.write('The optimal test order is:')
                    file_w.write(str(optimal_test_order[ii]))
                    file_w.write('\t')
                file_w.write('\n')

            file_w.write("\r")
            file_w.flush()

        file_w.close()


# A job means a test case in our case which including a set of attributes.
# 1) jobId is used to identify the job; 
# 2) maxRunTime means the max execution time for running the test case;
# 3) Requiredresource means the specific test resources required by a test case; 
# 4) Priority shows the priority for a test case (the value is simulated from 1 to 10 currently).


#give a template of the problem5
class Problem(object):
    NUMERICAL_TYPE = 0
    CATEGORICAL_TYPE = 1

    def getConstraints(self):
        pass

    def getFitness(self, v):
        pass


#Cisco's problem2
class Problem_scheduling(Problem):
    optimize = True

    def __init__(self):
        super(Problem, self).__init__()
        self.values = []
        self.jobsMin = 0
        self.jobsMax = 0
        self.jobs = []
        self.jobNum = 0
        self.resources = []

    def setresources(self, resources):
        self.resources = resources

    def getresources(self):
        return self.resources

    def getjobNum(self):
        return self.jobNum

    def setjobNum(self, jobNum):
        self.jobNum = jobNum

    def getValues(self):
        return self.values

    def setValues(self, values):
        self.values = values

    def setjobsMin(self, jobsMin):
        self.jobsMin = jobsMin

    def setjobsMax(self, jobsMax):
        self.jobsMax = jobsMax

    def setjobs(self, jobs):
        self.jobs = jobs

    def getConstraints(self):
        valuesOfConstraints = [[self.jobsMin, self.jobsMax, 0]]
        self.setValues(valuesOfConstraints)
        return self.values

    def Nor(self, n):
        m = float(n / (n + 1))
        return m

    def getFitness(self, v):
        countJobs = 0.0
        tm = 0.0  #fitness value
        temptime = 0  #calculating the whole time for the solution

        index = 0
        selectedjobs = []

        time_start = time.time()

        while index < v[0]:
            jobId = int(((self.jobsMax - 1) * random.random()) + 1)

            time_current = time.time()
            gap_of_time = time_current - time_start

            if gap_of_time <= 60:

                if self.jobs[jobId].jobId in selectedjobs:
                    continue

                tempjob = self.jobs[jobId]
                maxuploadcost = 0
                maxsubnetcost = 0
                sumweight = 0.0
                tempresources = tempjob.getRequiredResource()
                tag_of_record = True

                for i in range(len(tempresources)):

                    tempresource = tempresources[i]

                    if not tempresource.getisavailable():
                        tag_of_record = False
                        break
                    else:
                        tag_of_record = True

                    if tempresource.getcurrentbuild():
                        tempresource.uploadcost = 1
                    else:
                        tempresource.uploadcost = 6
                    if maxuploadcost < tempresource.getUploadcost():
                        maxuploadcost = tempresource.getUploadcost()
                    if maxsubnetcost < tempresource.getSubnetcost():
                        maxsubnetcost = tempresource.getSubnetcost()

                    sumweight = sumweight + tempresource.getWeight()
                    index = index + 1

                    temptime = temptime + tempjob.getMaxRunTime() + maxuploadcost + maxsubnetcost

                    numNorm = float(1 - self.Nor(tempjob.getPriority()))
                    tm += sumweight * (tempjob.getMaxRunTime() + maxuploadcost + maxsubnetcost) * numNorm
                    tm = self.Nor(tm)

                if tag_of_record:
                    selectedjobs.append(self.jobs[jobId].jobId)
                    for iii in range(len(tempresources)):
                        tempresources[iii].setisavailable(False)

            else:
                print "Out of time of finding all jobs!"
                break

        jobb = self.jobsMax - v[0]
        jobNor = float(jobb / self.jobsMax)

        countresource = 0
        for k in range(len(self.resources)):
            if self.resources[k].isavailable == True:
                countresource = countresource + 1

        resourceNor = float(countresource / len(self.resources))
        tm = float(tm / 3 + jobNor / 3 + resourceNor / 3)

        for kk in range(len(self.resources)):
            self.resources[kk].setisavailable(True)

        return selectedjobs


#the framework of the approach
class Search(object):
    def getSolution(self, problem):
        pass

    def getShortName(self):
        pass

    def __init__(self):
        self.time_threshold = long()
        self.start_time = long()
        self.delta = long()
        self.last_improvement = long()

        self.max_iterations = int()
        self.current_iteration = int()

    def search(self, problem):

        start_time = time.time()
        self.last_improvement = start_time

        if not self.hasStoppingCriterion():

            try:
                raise MyException(Exception)
            except MyException:
                print "No stopping criterion defined for " + self.getShortName()

        v = self.getSolution(problem)

        return v

    def validateConstraints(self, problem):

        c = problem.getConstraints()

        if not self.areConstraintsValid(c):

            try:
                raise MyException(Exception)
            except MyException:
                print "This Problem has invalid constraints"

    def areConstraintsValid(self, constraints):

        invalid = False

        if constraints is None or len(constraints) == 0:
            invalid = True
        else:
            for i in range(len(constraints)):
                if constraints[i] is None or (isinstance(constraints[i], list) and len(constraints[i]) != 3):
                    invalid = True
                    break
                if (isinstance(constraints[i], list) and constraints[i][0] > constraints[i][1]) or (
                                isinstance(constraints[i], list) and constraints[i][2] != 0 and constraints[i][2] != 1):
                    invalid = True
                    break

        return not invalid

    def isStoppingCriterionFulfilled(self):

        if self.max_iterations > 0:
            if self.current_iteration < self.max_iterations:
                return False

        if self.usingTime() and not self.isTImeExpired():
            return False

        if self.shouldKeepGoingBasedOnDelta():
            return False

        return True

    def increaseIteration(self):

        self.current_iteration += 1

    def getIteration(self):

        return self.current_iteration

    def hasStoppingCriterion(self):

        if self.max_iterations <= 0 and self.time_threshold <= 0 and self.delta <= 0:
            return False
        return True

    def setMaxIterations(self, maxIterations):

        self.max_iterations = maxIterations

    def usingTime(self):

        return self.time_threshold > 0

    def isTimeExpired(self):

        elapsed = time.time() - self.start_time
        return elapsed > self.time_threshold

    def normalise(self, x):

        if x < 0:

            try:
                raise MyException(Exception)
            except MyException:
                print "Cannot normalise negative value " + x

        return x / (x + 1.0)

    def setStopAfterMilliseconds(self, ms):

        self.time_threshold = ms

    def setKeepGoingIfBetterResults(self, d):

        self.delta = d

    def reportImprovement(self):

        self.last_improvement = time.time()

    def shouldKeepGoingBasedOnDelta(self):

        if self.delta <= 0:
            return False

        elapsed = time.time() - self.last_improvement

        return elapsed < self.delta


#SSGA approach------only preserve the used part
class SSGA(Search):
    population_size = int()
    xover_rate = float()

    def __init__(self, population_size=100, xover_rate=0.75):
        super(Search, self).__init__()
        self.population_size = population_size
        self.xover_rate = xover_rate


    def mutateAndEvaluateOffspring(self, ind, force_muatation):
        mutated = False
        cons = ind.problem.getConstraints()
        p = 1.0 / float(len(ind.v))

        while not mutated:
            if not force_muatation:
                mutated = True
            for i in xrange(len(ind.v)):

                if p >= random.random():
                    value = ind.v[i]

                    while value == ind.v[i]:
                        MIN = cons[i][0]
                        MAX = cons[i][1]
                        dif = MAX - MIN

                        if cons[i][2] == Problem.CATEGORICAL_TYPE:
                            value = MIN + random.randint(0, dif)
                        else:
                            step = dif / 100.0
                            if random.randint(0, 0xff) % 2 == 0:
                                sign = -1
                            else:
                                sign = 1
                            delta = sign * (1 + int(step * random.random()))
                            k = ind.v[i] + delta
                            if k > MAX:
                                k = MAX
                            if k < MIN:
                                k = MIN
                            value = k
                    ind.v[i] = value
                    mutated = True

        ind.evaluate()
        self.increaseIteration()


# Class for search algorithms
# (1+1) Evolutionary Algorithm Implementations
class OpOEA(SSGA):
    def __init__(self):
        super(SSGA, self).__init__()

    def getSolution(self, problem):
        current = getRandomIndividual(problem)
        current.evaluate()
        self.increaseIteration()

        if current.fitness_value == 0.0:
            return current.v

        tmp = getRandomIndividual(problem)

        while not self.isStoppingCriterionFulfilled():
            tmp.copyDataFrom(current)
            self.mutateAndEvaluateOffspring(tmp, True)

            if tmp.fitness_value == 0.0:
                return tmp.v

            if tmp.fitness_value <= current.fitness_value:
                current.copyDataFrom(tmp)
                if tmp.fitness_value < current.fitness_value:
                    self.reportImprovement()

        return current.v

    def getShortName(self):
        return "OpOEA"


class Job():
    def __init__(self):
        self.jobId = int()
        self.maxRunTime = int()
        self.taskId = int()
        self.list = []
        self.size = int()
        self.priority = int(random.random() * 9 + 1)
        self.requiredresource = []

    def getJobId(self):
        return self.jobId

    def setJobId(self, jobId):
        self.jobId = jobId

    def getMaxRunTime(self):
        return self.maxRunTime

    def setMaxRunTime(self, maxRunTime):
        self.maxRunTime = maxRunTime

    def getTaskId(self):
        return self.taskId

    def setTaskId(self, taskId):
        self.taskId = taskId

    def getList(self):
        return self.list

    def getSize(self):
        return self.size

    def setSize(self, size):
        self.size = size

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def getRequiredResource(self):
        return self.requiredresource

    def setRequiredResource(self, requiredresource):
        self.requiredresource = requiredresource


#Resource means the test resources in the pool including a set of attributes.
#1) resourceid is used to identify a particular resource; 
#2) weight is used to represent the weight of a test resource based on the available number of test resources in the pool and associated #features; 
#3) currentbuild shows if the test resource is in the current setting up, if the currentbuild is true, the uploadcost will be 1 min. If the currentbuild is false, the uploadcost will be 6 mins for e20/snoopy and 4 mins for the others (the cost value can be changed); 
#4) subnetcost shows the cost for setting up correct subnet and the current value is simulated from 0 mins to 10 mins;
#5) isavailable is used to identify the availability of a test resource. 

class Resource():
    def __init__(self):
        self.resourceid = int()
        self.weight = float()
        self.currentbuild = bool()
        self.uploadcost = int()
        self.subnetcost = int()
        self.isavailable = bool()
        self.subnetcost = int(random.random() * 10)

    def getResourceId(self):
        return self.resourceid

    def setResourceId(self, resourceid):
        self.resourceid = resourceid

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getUploadcost(self):
        return self.uploadcost

    def setUploadcost(self, uploadcost):
        self.uploadcost = uploadcost

    def getSubnetcost(self):
        return self.subnetcost

    def setSubnetcost(self, subnetcost):
        self.subnetcost = subnetcost

    def getisavailable(self):
        return self.isavailable

    def setisavailable(self, isavailable):
        self.isavailable = isavailable

    def getcurrentbuild(self):
        return self.currentbuild


#used in DataReader, to transform the string True or False to the True and False
def to_bool(value):
    """
        Converts 'something' to boolean. Raises exception for invalid formats
        Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
        Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if value.lower() in ("true\n", "true"): return True
    if value.lower() in ("false\n", "false"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


# The classes below are the classes that are used in the (1+1) EA algorithm.
class Individual():
    def __init__(self, p):
        self.v = []
        self.fitness_value = float()
        self.problem = p

    def compareTo(self, other):
        if self.fitness_value == other.fitness_value:
            return 0
        elif self.fitness_value > other.fitness_value:
            return 1
        else:
            return -1

    def evaluate(self):
        self.fitness_value = self.problem.getFitness(self.v)

    def getCopy(self):
        Copy = Individual(self.problem)
        Copy.v = copy.deepcopy(self.v)
        copy.fitness_value = self.fitness_value
        return Copy

    def copyDataFrom(self, other):
        self.problem = other.problem
        self.v = copy.deepcopy(other.v)
        self.fitness_value = other.fitness_value


#method used to get a random case
def getRandomIndividual(p):
    ind = Individual(p)
    constraints = p.getConstraints()
    ind.v = [0] * len(constraints)

    for i in range(len(ind.v)):
        Min = constraints[i][0]
        Max = constraints[i][1]
        Type = constraints[i][2]

        dif = Max - Min

        k = random.randint(0, dif)

        ind.v[i] = Min + k
        if ind.v[i] == 0:
            print ""
    ind.evaluate()
    return ind


#used in Search
class MyException(Exception):
    pass


if __name__ == '__main__':
    main()


