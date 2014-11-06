from collections import defaultdict
from Jobscheduling_Cisco import Job, Resource, BookingFailed
from dateutil.parser import parse as parse_date

class FeatureMap(object):
    def __init__(self, resources):
        self.features = defaultdict(set)
        self.types = defaultdict(set)
        self.groups = defaultdict(set)
        self.resources = []
        self.cache = {}

        for resource in resources:
            self.add(resource)

    def add(self, resource):
        for feat in resource.features:
            self.features[feat].add(resource)
        for type in resource.types:
            self.types[type].add(resource)
        for group in resource.groups:
            self.groups[group].add(resource)

    def filter(self, required, group):
        key = [group, required['type'], ]
        if 'features' in required:
            key.extend(required['features'])
        key = tuple(key)
        if key in self.cache:
            return self.cache[key]

        res = list(self._filter(required, group))
        res.sort(lambda a, b: cmp(len(a.features), len(b.features)))
        self.cache[key] = res
        return res

    def _filter(self, required, group):
        base = self.types[required['type']].copy()
        l = len(base)
        if group is not None:
            base.intersection_update(self.groups[group])
        l = l - len(base)
        if 'features' in required:
            for feature in required['features']:
                base.intersection_update(self.features[feature])
        return base

    def find_required_resources(self, requirements, group):
        results = []
        success = True
        for req in requirements:
            tmp = self.filter(req, group)
            for ep in tmp:
                if ep.isavailable:
                    break
            else:
                success = False
                break
            ep.isavailable = False
            results.append(ep)
        for ep in results:
            assert group in ep.groups
            ep.isavailable = True
        if not success:
            return None
        return results

class MyJob(Job):
    def __init__(self, _map):
        super(MyJob, self).__init__()
        self._map = _map

    def getRequiredResource(self):
        res = self._map.find_required_resources(self.requiredresource, self.group)
        if res is None:
            raise BookingFailed()
        return res

def make_job(task, *args):
    j = MyJob(*args)
    j.jobId=task['id']
    j.priority = task['priority']
    j.requiredresource = task['required']
    j.maxRunTime = task['max_runtime']
    if 'group' in task:
        j.group = task['group']
    if 'add_time' in task:
        j.add_time = int(parse_date(task['add_time']).strftime("%s"))
    if 'started' in task:
        j.started = int(parse_date(task['started']).strftime("%s"))
    if 'duration' in task:
        if task['duration'] is None:
            j.duration = None
        else:
            j.duration = int(task['duration'])
    return j

def make_resource(res):
    r = Resource()
    r.resourceid = res['id']
    r.type = res['type']
    r.types = res['types']
    r.features = set(res['features'])
    r.groups = res['groups']
    r.currentbuild = '0'
    r.uploadcost = 10
    r.subnetcost = 0
    r.isavailable = True
    return r
