import time
import datetime
import json
from itvm_pool import *
import sys
import logging
import csv
import os
log = logging.getLogger("simitvm")
logging.basicConfig()

class ItvmSimulator(object):
    def __init__(self, resources, tasks, search, output):
        self.resources = resources
        self.future_tasks = tasks
        self.future_tasks.sort(lambda a,b: cmp(a.add_time, b.add_time))
        self.search = search
        self.output = output

        self.runnable = []
        self.running = []
        self.completed = []
        self.clock = tasks[0].add_time

        self.next_planner_tick = None
        self.planner_time = 120

        self.start = self.clock

    def check_add_tasks(self):
        """
        Check if the clock has gone past the time a task were scheduled.
        """
        new_tasks = []
        count = 0
        for task in list(self.future_tasks):
            if task.add_time <= self.clock:
                count += 1
                self.runnable.append(task)
                new_tasks.append(task)
                self.future_tasks.remove(task)
            else:
                break
        return new_tasks

    def free_finished(self):
        """
        Free the resources of tasks that's done.
        """
        completed = []
        for time, job in self.running:
            if time <= self.clock:
                for resource in job.chosenResources:
                    resource.isavailable = True
                completed.append((time, job))
        for time, job in completed:
            self.completed.append((self.clock, job))
            self.running.remove((time, job))

    def try_start(self, tasks=None):
        """
        See if there are any stasks that can be started. I've seen the search algorithm return a
        subset of the tasks that can be run so do a little loop just to test.
        """
        # only pass the available resources to the searches
        available_resources = filter(lambda x: x.isavailable, self.resources)

        if tasks is not None:
            # if we have a subset of the tasks to search
            to_run = self.search(available_resources, tasks)
        else:
            # else do them all.
            to_run = self.search(available_resources, self.runnable)
        if len(to_run) == 0:
            return

        for test in to_run:
            assert test.duration > 0
            finish = self.clock + test.duration
            assert finish > self.clock
            self.running.append((finish, test))

            for resource in test.chosenResources:
                resource.isavailable = False
            if tasks:
                tasks.remove(test)
            self.runnable.remove(test)
        self.running.sort(lambda a, b: cmp(a[0], b[0]))

    def next_clock_action(self):
        """
        Figure out when the next event is. It can be new tasks that have been scheduled,
        tasks that's finished so that we have free resources or planner ticks if it's
        set up to do that.
        """
        times = []
        if self.future_tasks:
            times.append((self.future_tasks[0].add_time, 'new'))
        if self.running:
            times.append((self.running[0][0], 'finish'))
        if len(self.runnable) > 0 and self.next_planner_tick is not None:
            times.append((self.next_planner_tick, 'planner'))
        if not times:
            return None
        times.sort(lambda a,b: cmp(a[0], b[0]))
        return times[0][0]

    def run(self):
        """
        The main loop, does stuff and advances time until we're all done.
        """
        f = open(self.output, 'w')
        csv_w = csv.writer(f)
        row = ['time', 'future', 'runnable', 'running', 'completed', 'resources']
        csv_w.writerow(row)
        print ', '.join(row)

        iteration = 0
        try:
            while self.clock:
                self.free_finished() # first free finished resources

                new_tasks = self.check_add_tasks() # add tasks that have been scheduled

                if self.next_planner_tick is None or self.clock >= self.next_planner_tick:
                    self.try_start() # try to runnable tasks
                    if self.next_planner_tick is not None:
                        self.next_planner_tick += self.planner_time

                # dump to csv
                row = [datetime.datetime.fromtimestamp(self.clock),
                        len(self.future_tasks),
                        len(self.runnable),
                        len(self.running),
                        len(self.completed),
                        len(filter(lambda x: x.isavailable, self.resources))]
                csv_w.writerow(row)
                if iteration % 400 == 0:
                    print ', '.join(map(str, row))

                # figure out the next tick
                self.last_clock = self.clock
                next = self.next_clock_action()
                if next is None:
                    break
                self.clock = next
                iteration += 1
        finally:
            f.close()
        print
        print "Duration: %d" % (self.last_clock - self.start)


from Jobscheduling_Cisco import CiscoJobSchedulingExecute
def search_0_plus_0(resources, jobs):
    # scheduling search
    scheduling = CiscoJobSchedulingExecute(jobs,
                                           resources,
                                           0,
                                           len(jobs),
                                           loopNum=1)
    res = scheduling.search(MaxIterations=50)
    return [x[0] for x in res]


def fcfs(resources, jobs):
    # just pick all tasks that can be ran.
    res = []
    tresources = []
    for job in jobs:
        try:
            tmp = job.getRequiredResource()
        except BookingFailed:
            continue
        if tmp:
            for t in tmp:
                t.isavailable = False
            tresources.extend(tmp)
        res.append(job)
        job.chosenResources = tmp
    return res


def main():
    if len(sys.argv) == 1:
        print "Usage: sim_itvm.py <output.csv> [fcfs]"
        sys.exit(1)

    if not os.path.exists('resources.json'):
        print "resources.json not found"
        sys.exit(1)
    resources = json.load(open('resources.json'))
    resources = map(make_resource, resources)
    _map = FeatureMap(resources)

    if not os.path.exists('tasks.json'):
        print "tasks.json not found"
        sys.exit(1)
    tasks = json.load(open('tasks.json'))
    jobs = map(lambda x: make_job(x, _map), tasks)
    jobs.sort(lambda a, b: cmp(a.add_time, b.add_time))
    jobs = filter(lambda x: x.duration is not None, jobs)

    print "Total tasks: %d" % len(jobs)
    def is_bookable(task):
        try:
            task.getRequiredResource()
            return True
        except BookingFailed:
            return False
    jobs = filter(is_bookable, jobs)
    print "Bookable jobs: %d" % len(jobs)

    output = sys.argv[1]

    if 'fcfs' in sys.argv:
        print "Using fcfs"
        search_to_use = fcfs
    else:
        print "Using 0+0 search"
        search_to_use = search_0_plus_0
    itvm = ItvmSimulator(resources, jobs, search_to_use, output)
    itvm.run()

if __name__ == '__main__':
    main()
