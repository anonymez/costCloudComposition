import time
from experiments.costants import print_request,FUNCTIONALITIES,sort_print
from experiments.requests import REQUESTS
from experiments.window import WINDOW
from experiments.deployer import deploy,iterative_optimim_deploy
from experiments.CloudService import CloudService,CSID
from experiments.migration import migrate
from experiments.tomigrate import MIGRATION

if __name__ == "__main__":
    print ("Fuzzy-based cost-aware deployment of Certified Composite Service for the Cloud - WINDOW"+str(WINDOW))
    csi = []
    cid=CSID()
    #new_cs=CloudService(csid=cid,property_name="p1",property_level=2,f="f1")
    #csi.append(new_cs)
    matrix_D = []
    nreq = 0;

    for k in range(0,len(REQUESTS)-WINDOW+1):

        slide = []
        print ("------------------------------------\n\nWindow t="+str(k)+" :")
        for i in range(k,k+WINDOW):

            REQUESTS[i][0]["t"] = i
            print(print_request(REQUESTS[i]))
            slide.append(REQUESTS[i])
        #print "\n\nWindow"+ str(slide)
        #divide by functionalities requests and services
        csi_by_f={}
        slide_by_f={}
        for f in FUNCTIONALITIES:
            csi_by_f[f]=[]
            slide_by_f[f]=[]
        #csi_by_f={"f1":[],"f2":[],"f3":[],"f4":[]}
        for cs in csi:
           csi_by_f[cs.get_functionality()].append(cs)


        #slide_by_f={"f1":[],"f2":[],"f3":[],"f4":[]}
        r_index=0
        for r in slide:
            for single_r in r:
                single_r["time"]=r_index
                slide_by_f[single_r["f"]].append(single_r)
                for pr in range(0,single_r["p"]["level"]+1):
                    cs_app=CloudService(csid=cid,property_name=single_r["p"]["name"],property_level=pr,f=single_r["f"])
                    csi_by_f[single_r["f"]].append(cs_app)
            r_index+=1
        result={}
#debug point
        if k==108:
            print ("DEBUG")

        start_time = time.time()
        for f in FUNCTIONALITIES:
            if len(slide_by_f[f])>0 and slide_by_f[f][0]["time"]==0 :
                result[f]=(deploy(csi_by_f[f],slide_by_f[f],f))
                if result[f] is not None:
                    new = True
                    for cs in csi:
                        if cs.is_equal(result[f]):
                            new = False
                            break
                    if new == True:
                        print ("added new Cloud Service :"+ result[f].get_id())

                        if MIGRATION:
                            migrate(result[f],csi)
                        csi.append(result[f])

        execution_time=time.time() - start_time
        print ("\n\n")
        for f in FUNCTIONALITIES:
            to_print=[]
            for cs in csi:
                if cs.get_functionality() == f:
                    to_print.append(cs)
            sort_print(to_print)
        tc=0
        for c in csi:
            tc+=c.get_total_cost()
        print("TOTAL COST: "+str(tc))
        print("Executed in %s seconds ---" % (execution_time))
