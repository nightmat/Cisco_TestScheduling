__author__ = 'Ruihua and Shuai'

import random
import string
import logging
import time
import copy
import math
import sys

class BookingFailed(Exception):
    pass

log = logging.getLogger("Scheduling")
#logging.basicConfig(level=logging.INFO)#DEBUG)

#the main programme

def main():

    jobs = []  # input: initialise test job list
    resources = []  # input: initialise test resource list
    scheduled_jobs = []  # output: test job list with an order

    # main function for getting the scheduled test jobs
    ex = CiscoJobSchedulingExecute(jobs=jobs, resources=resources,
                                   jobsMin=1, jobsMax=len(jobs))
    scheduled_jobs = ex.getValues_1()  # the scheduled test jobs are outputted here


#The main class for scheduling:

class CiscoJobSchedulingExecute():

    def __init__(self, jobs=[], resources=[], jobsMin=0, jobsMax=0, loopNum=1):
        self.jobs = jobs  # test jobs
        self.resources = resources  # test resources
        self.values = []
        self.jobsMin = jobsMin
        self.jobsMax = jobsMax
        self.loopNum = loopNum

    def search(self, MaxIterations=500):
        algorithms = [OpOEA()]

        for search_algorithm in algorithms:
            for k in range(self.loopNum):
                p = Problem_scheduling()  # initialise the Cisco test scheduling problem
                p.setresources(self.resources)  # set the initialised test resources
                p.setjobs(self.jobs)  # set the initialised test jobs
                p.setjobsMin(self.jobsMin)  # set the minimum of number of outputted jobs, which is 1
                p.setjobsMax(self.jobsMax)  # set the maximum of number of outputted jobs, which is the length of input test job list
                search_algorithm.setMaxIterations(MaxIterations)
                search_algorithm.setStopAfterMilliseconds(10 * 1000)
                t = Search()
                t.validateConstraints(p)
                variables = search_algorithm.search(p)

                optimal_test_order, fitness = p.getFitness(variables)
                return optimal_test_order


#The below codes are used to defined the scheduling problem for calculating the fitness function
#define an abstract for a general problem

class Problem(object):
    NUMERICAL_TYPE = 0
    CATEGORICAL_TYPE = 1

    def getConstraints(self):
        pass

    def getFitness(self, v):
        pass

#Define Cisco's scheduling problem

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

    def calculateFitness(self, jobs):
        """
        Stubbed out fitness calculation for testing, not in use right now but maybe we should use it in getFitness.
        """
        sumweight = 0
        calculated_fitness = 0
        for job in jobs:

            maxuploadcost = 0
            maxsubnetcost = 0
            for tempresource in job.chosenResources:
                if tempresource.getcurrentbuild() == job.revision:
                    tempresource.uploadcost = 1
                else:
                    tempresource.uploadcost = 6
                if maxuploadcost < tempresource.getUploadcost():
                    maxuploadcost = tempresource.getUploadcost()
                if maxsubnetcost < tempresource.getSubnetcost():
                    maxsubnetcost = tempresource.getSubnetcost()
                sumweight += tempresource.getWeight()
            numNorm = float(1 - self.Nor(job.getPriority()))
            calculated_fitness += sumweight * (job.getMaxRunTime() + maxuploadcost + maxsubnetcost) * numNorm

        calculated_fitness = self.Nor(calculated_fitness)
        job_count_fitness = 1 - (len(jobs) / float(self.jobsMax))

        countresource = len([r for r in self.resources if r.isavailable])

        resourceNor = float(countresource) / len(self.resources)
        calculated_fitness = (float(calculated_fitness) / 3 +
                              float(job_count_fitness) / 3 +
                              float(resourceNor) / 3)

        for resource in self.resources:
            resource.setisavailable(True)

        return calculated_fitness

    def getFitness(self, v):
        countJobs = 0.0
        tm = 1.0  #fitness value
        temptime = 0  #calculating the whole time for the solution
        calculated_fitness = 0.0

        index = 0
        selectedjobs = []
        #random.seed(v[0])
        choosable_jobs = {j: j.jobId for j in self.jobs}
        #while jobs_scheduled_count < v[0]:
        #print "\n" * 5
        log.debug("Choosable jobs, %r", choosable_jobs)
        log.debug("Resources, %r", self.resources)
        used_resources = []
        while len(choosable_jobs) and len(selectedjobs) < v[0]:
            tempjob = random.choice(choosable_jobs.keys())

            del choosable_jobs[tempjob]
            log.debug("After pick jobs, %r", choosable_jobs)
            log.debug("Trying to schedule %r", tempjob)

            maxuploadcost = 0
            maxsubnetcost = 0
            sumweight = 0.0
            try:
                tempresources = tempjob.getRequiredResource()
                log.debug("Success booking %r", tempjob)
            # 
            #     tempresources = self.findPossibleResources(
            #         temprequiredresources, tempjob)
            except BookingFailed:
                log.debug("Booking resources for %r failed" % tempjob)
                continue

            selectedjobs.append((tempjob, tempresources))

            for tempresource in tempresources:
                if tempresource.getcurrentbuild():
                    tempresource.uploadcost = 1
                else:
                    tempresource.uploadcost = 6
                if maxuploadcost < tempresource.getUploadcost():
                    maxuploadcost = tempresource.getUploadcost()
                if maxsubnetcost < tempresource.getSubnetcost():
                    maxsubnetcost = tempresource.getSubnetcost()

                sumweight += tempresource.getWeight()

            numNorm = float(1 - self.Nor(tempjob.getPriority()))
            calculated_fitness += sumweight * (tempjob.getMaxRunTime() + maxuploadcost + maxsubnetcost) * numNorm

            tempjob.chosenResources = tempresources
            for temp in tempresources:
                temp.setisavailable(False)

        if len(selectedjobs) == 0:
            return [], 1.0

        calculated_fitness = self.Nor(calculated_fitness)
        job_count_fitness = 1 - (len(selectedjobs) / float(self.jobsMax))

        countresource = len([r for r in self.resources if r.isavailable])

        resourceNor = float(countresource) / len(self.resources)
        calculated_fitness = (float(calculated_fitness) / 3 +
                              float(job_count_fitness) / 3 +
                              float(resourceNor) / 3)

        for resource in self.resources:
            resource.setisavailable(True)

        log.info("[%s] Managed selection with %s jobs (fitness: %s)",
                 v, len(selectedjobs), calculated_fitness)
        return selectedjobs, calculated_fitness


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

            raise RuntimeError("No stopping criterion defined for " + self.getShortName())


        self.current_iteration = 0

        v = self.getSolution(problem)

        return v

    def validateConstraints(self, problem):

        c = problem.getConstraints()

        if not self.areConstraintsValid(c):
            raise RuntimeError("This Problem has invalid constraints")

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

        if self.usingTime() and not self.isTimeExpired():
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
            raise RuntimeError("Cannot normalise negative value %s" % x)
        return x / (x + 1.0)

    def setStopAfterMilliseconds(self, ms):

        self.time_threshold = ms

    def setKeepGoingIfBetterResults(self, d):

        self.delta = d

    def reportImprovement(self, v):
        self.last_improvement = time.time() 
        self.best_arguments = v

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

    def mutateAndEvaluateOffspring(self, individual, force_muatation):
        mutated = False
        constraints = individual.problem.getConstraints()
        random.seed()

        while not mutated:
            if not force_muatation:
                mutated = True
            for i, argument in enumerate(individual.v[:]):
                old_argument = int(argument)
                while argument == old_argument:
                    MIN = constraints[i][0]
                    MAX = constraints[i][1]
                    diff = MAX - MIN
                    if diff == 0:
                        mutated = True
                        break
                    step = diff / 100.0
                    sign = random.choice([1, -1])
                    delta = sign * (1 + int(step * random.random()))
                    new_argument = argument + delta
                    if new_argument > MAX:
                        new_argument = MAX
                    if new_argument < MIN:
                        new_argument = MIN
                    argument = new_argument
                individual.v[i] = argument
                mutated = True
        individual.evaluate()
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

        best_fitness = current.fitness_value[1]
        self.reportImprovement(current.v[:])

        while not self.isStoppingCriterionFulfilled():
            self.mutateAndEvaluateOffspring(current, True)
            current_fitness = current.fitness_value[1]

            if current_fitness == 0.0:
                return current.v

            #log.debug("Current fitness: %f\tbest fitness: %f", current_fitness, best_fitness)
            #print [a[0] for a in current.fitness_value[0]]
            if current_fitness < best_fitness:
                log.info('Fitness improved - new fitness %s - best fitness was %s', current_fitness, best_fitness)
                best_fitness = current_fitness
                self.reportImprovement(current.v[:])

        return self.best_arguments

    def getShortName(self):
        return "OpOEA"


# A job means a test job in our case which including a set of attributes.
# 1) jobId is used to identify the job;
# 2) maxRunTime means the max execution time for running the test job;
# 3) requiredresource means the specific test resources required by a test job;
# 4) Priority shows the priority for a test job (the value is simulated from 1 to 10 currently).

class Job(object):
    def __init__(self):
        self.jobId = int()
        self.maxRunTime = int()
        self.taskId = int()
        self.task = None
        self.priority = 1.0 #int(random.random() * 9 + 1)
        self.requiredresource = []
        self.chosenResources = []

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

    def __repr__(self):
        return '<job id:%d %d>' % (self.jobId, self.maxRunTime)


# Resource means the test resources in the pool including a set of attributes.
# 1) resourceid is used to identify a resource;
# 2) weight is used to represent the weight of a test resource based on the
#    available number of test resources in the pool and associated #features;
# 3) currentbuild shows if the test resource is in the current setting up,
#    if the currentbuild is true, the uploadcost will be 1 min. If the
#    currentbuild is false, the uploadcost will be 6 mins for e20/snoopy and
#    4 mins for the others (the cost value can be changed);
# 4) subnetcost shows the cost for setting up correct subnet and the current
#    value is simulated from 0 mins to 10 mins;
# 5) isavailable is used to identify the availability of a test resource.

class Resource():
    def __init__(self, resourceid=1, weight=1.0, currentbuild=False, uploadcost=0, subnetcost=0, isavailable=True):
        self.resourceid = resourceid
        self.weight = weight
        self.currentbuild = currentbuild
        self.uploadcost = uploadcost
        self.subnetcost = subnetcost
        self.isavailable = isavailable

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

    def __repr__(self):
        return '<res %d %s>' % (self.resourceid, self.isavailable)


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
        #if ind.v[i] == 0:
        #    print ""
    #ind.evaluate()
    return ind


#used in Search
class MyException(Exception):
    pass


if __name__ == '__main__':
    main()


