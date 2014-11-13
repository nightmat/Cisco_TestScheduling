jobs = []
NUM_TASKS = 1000
for i in range(NUM_TASKS):
    job = {'id':i,
           'priority':1.0 if i < NUM_TASKS / 2 else 10.0,
           'required':[{'type':1}, {'type':1}],
           'max_runtime':60}
    jobs.append(job)

import random
random.shuffle(jobs)

resources = []
for i in range(NUM_TASKS):
    resource = {'id':i,
                'type':1,
                'features':[]}
    resources.append(resource)




from itvm_pool import *

resources = map(make_resource, resources)

_map = FeatureMap(resources)

jobs = map(lambda x: make_job(x, _map), jobs)

from Jobscheduling_Cisco import CiscoJobSchedulingExecute
scheduling = CiscoJobSchedulingExecute(jobs,
                                       resources,
                                       70, 
                                       len(jobs),
                                       loopNum=1)
res = scheduling.search()


priorities = []

for job, endpoints in res:
    for ep in endpoints:
        ep.setisavailable(False)
    priorities.append(job.priority)

available_endpoints = filter(lambda x: x.isavailable, resources)


print "Average priority", sum(priorities) / len(priorities)
print "Scheduled tasks", len(res)
print "task total", len(jobs)
print "Available:", len(available_endpoints)
print "Not available:", len(resources) - len(available_endpoints)
