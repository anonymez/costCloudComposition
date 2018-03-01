import re
import six

import subprocess

from pip._vendor.appdirs import unicode

from costants import DIRECT_COST,INDIRECT_COST, MISMATCH_COST
from fcost import fcost

class CSID:
    def __init__(self):
        self.uuid=0

    def get_id(self):
        self.uuid = self.uuid+1
        return self.uuid

class Property:
    def __init__(self,name,level):
        self.name=name
        self.level=level

    def compare(self,property):
        #if(self.name == property.name):
        return self.level-property.level
        #else:
            #raise Exception('non comparable')

class CloudService:

    def get_property(self):
        return self.property

    def get_functionality(self):
        return self.functionality

    def get_id(self):
        return self.uuid

    def clear_window(self):
        self.window=[]

    def add_request_window(self,request):
        self.window.append(request)

    def add_requests_window(self,requests):
        self.window=requests

    def get_total_cost(self):
        tc=0
        for cost in self.costfc:
            tc+=cost
        return tc

    def __init__(self, f,csid,property_name, property_level):
        self.window=[]
        code=str(csid.get_id())
        for x in range(len(code),3):
            code="0"+code
        self.uuid="I"+code
        self.k=0
        self.functionality=f
        self.requests=[]
        self.costfc=[]
        self.property=Property(name=property_name,level=property_level)
        for cost in DIRECT_COST:
            if cost["f"] == self.functionality and cost["p"]["name"] == property_name and cost["p"]["level"] == property_level:
                self.direct_cost=cost["fcost"]
        for cost in INDIRECT_COST:
            if cost["f"] == self.functionality and cost["p"]["name"] == property_name and cost["p"]["level"] == property_level:
                self.indirect_cost=cost["fcost"]
        for cost in MISMATCH_COST:
            if cost["f"] == self.functionality and cost["p"]["name"] == property_name and cost["p"]["level"] == property_level:
                self.mismatch_cost=cost["fcost"]

    def addRequest(self,request):
        try:
            if self.property.compare(Property(request["p"]["name"],request["p"]["level"])) >=0 :
                self.k+=1
                self.requests.append(request)
                d_cost = self.direct_cost[self.k]
                i_cost = self.indirect_cost[self.k]
                m_cost = self.mismatch_cost[request["p"]["level"]]
                stdout = fcost[self.k][self.property.level][request["p"]["level"]]
                self.costfc.append(stdout)
                #stdout = subprocess.check_output(
                #    'java -jar /Users/iridium/IdeaProjects/fuzzyProject/out/artifacts/fuzzyProject_jar/fuzzyProject.jar' + ' -d ' + str(
                #        d_cost) + ' -i ' + str(i_cost) + ' -m ' + str(m_cost), shell=True)
                #stdout = re.findall("\d+\.\d+", str(stdout))
                #self.costfc.append(float(stdout[0]))
                return self.k
        except Exception as exp:
            return -1

    def is_equal(self,cs):
        if self.uuid == cs.get_id():
            return True
        return False

    def get_window_cost(self):
        ndeploy = self.k
        tc_window=0
        for r in self.window:
            ndeploy += 1
            stdout = fcost[ndeploy][self.property.level][r["p"]["level"]]
            tc_window += stdout
        return tc_window



    def window_delete(self):
        app=self.window[0]
        self.window=[]
        for r in self.requests:
            if r!=app:
                self.window.append(r)
        tc=0
        for k in range(0,len(self.window)):
            tc += fcost[k+1][self.property.level][self.window[k]["p"]["level"]]
        return tc
        #stdout = fcost[self.k][self.property.level][request["p"]["level"]]
        #return stdout


    def delete(self,request):
        app=[]
        for r in self.requests:
            if r!=request:
                app.append(r)
        self.requests=app
        #tc=0
        self.costfc=[]
        for k in range(0,len(self.window)):
            stdout= fcost[k+1][self.property.level][self.window[k]["p"]["level"]]
            self.costfc.append(stdout)
        self.k=len(self.requests)
        #return tc
        #stdout = fcost[self.k][self.property.level][request["p"]["level"]]
        #return stdout



    def getNextCost(self,requests=None):
        if requests is None:
            requests= self.window
        #delta = len(requests)
        ndeploy = self.k

        #m_cost=[]
        #for r in requests:
        #     for v in self.mismatch_cost:
        #         if v["deploy"] == self.property.level and v["request"] == r["p"]["level"]:
        #             m_cost.append=v["cost"]
        tc_cs = 0
        for r in requests:
            ndeploy+=1
            try:
                #d_cost = self.direct_cost[ndeploy]
                #i_cost = self.indirect_cost[ndeploy]
                #m_cost = self.mismatch_cost[r["p"]["level"]]

                stdout = fcost[ndeploy][self.property.level][r["p"]["level"]]


            #stdout = subprocess.check_output('java -jar /Users/iridium/IdeaProjects/fuzzyProject/out/artifacts/fuzzyProject_jar/fuzzyProject.jar'+' -d '+str(d_cost)+' -i '+str(i_cost)+' -m '+str(m_cost), shell=True)
            #stdout=re.findall("\d+\.\d+", str(stdout))
            #print stdout
                tc_cs+=stdout
            except Exception as inst:
                print("Exception")
            #if len(stdout) == 1:
            #    tc_cs+=float(stdout[0])
        for fc in self.costfc:
            tc_cs+=fc
        #d_cost, i_cost, m_cost
        #tc_cs+new cost
        return tc_cs

    def check_deploy(self,request):
        if self.property.compare(Property(request["p"]["name"], request["p"]["level"])) >= 0:
            return True
        else:
            return False

    def __str__(self):
        requests_to_print=0
        for r in self.requests:
            if r["p"]["level"]< self.property.level:
                requests_to_print+=1
        result = self.uuid + ": \t{functionality: "+self.functionality+" property: "+str(self.property.level) + " requests: " + str(self.k)+" , mismatch request: "+ str(requests_to_print)+"}"
        return result

    def __unicode__(self):
        if six.PY3:
            return str(self._text)
        else:
            return unicode(self._text)
def parse_compatible(candidate,csi,requests):
    request=0
    for d in candidate:
        cs=d.index(1)

        compatible=csi[cs].check_deploy(requests[request])
        if compatible == False:
            return False
        request+=1
    return True

if __name__ == "__main__":
    a=[[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    parse_compatible(candidate=a,csi=None,requests=None)