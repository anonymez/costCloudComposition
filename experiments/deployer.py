import math
import multiprocessing

from partitionset import partition_set_smart,partition_set_optimum
from CloudService import parse_compatible,CloudService,CSID
from fcost import fcost
from costants import MAX_P

from combination import recursive

N_PROC=4

def cut_candidates(all_candidates,start, end, to_delete,csi,requests):
    print ("cutting candidates")
    index = start
    for i in range(start,end):
        candidate=all_candidates[i]
        to_keep = parse_compatible(candidate=candidate, csi=csi, requests=requests)
        if to_keep == False:
            to_delete.append(index)
        index+=1
    print ("end")


def check_float(a,b):
    if math.isclose(a,b):
        return 0
    else:
        return a-b



def deploy(csi,requests,f=None):


    print ("Analyzing functionality: "+f)
    if len(requests) == 0:
        print  ("no request")
        return None
    #to_deploy=len(csi)+len(requests)

    #print csi
    #print requests

    deletere=[]
    r_index=0
    for r in requests:
        r_csi=0
        for c in csi:
            if c.check_deploy(r)==False:
              deletere.append([r_index,r_csi])
            r_csi+=1
        r_index+=1
    candidate_matrix=partition_set_smart(window=len(requests),matrix_d=len(csi),deleter=deletere)
    #TODO: check sostitution
    if len(requests) == 1:
        cc=[]
        for c in candidate_matrix:
           cc.append([c])
        candidate_matrix=cc
    index=0
    to_delete=[]
    l_candidate = len(candidate_matrix)
    print ("Number of candidate tot:"+str(l_candidate))
    #start=[]
    #end=[]
    #result = []
    #factor=int(l_candidate/N_PROC)
    #end_d=0
    #for pid in range (0,N_PROC):
    #    result.append([])
    #    if pid==0:
    #        start.append(0)
    #        end_d+=factor
    #        end.append(end_d)
#
    #    elif pid == N_PROC-1:
    #        start.append(end_d)
    #        end_d += factor
    #        end.append(l_candidate)
    #    else:
    #        start.append(end_d)
    #        end_d += factor
    #        end.append(end_d)
#
    #jobs = []
#
    #for pid in range(0,N_PROC):
    #    p = multiprocessing.Process(target=cut_candidates,args=(candidate_matrix,start[pid],end[pid],result[pid],csi,requests) )
    #    jobs.append(p)
    #    p.start()
#
    #for proc in jobs:
    #    proc.join()
    #for pid in range(0,N_PROC):
    #    to_delete+=result[pid]

    candidate=candidate_matrix

    #for candidate in candidate_matrix:
    #    to_keep=parse_compatible(candidate=candidate,csi=csi,requests=requests)
    #    if to_keep == False:
    #        to_delete.append(index)
    #    index+=1
    #candidate = [i for j, i in enumerate(candidate_matrix) if j not in to_delete]



    for cs in csi:
        cs.clear_window()
    ref=None
    result_candidate=None
    print ("Number of candidate:"+str(len(candidate)))
    #cutting branch
    for c in candidate:
        selected_cs=[]
        r=0
        for set_cs in c:
            cs = set_cs.index(1)
            csi[cs].add_request_window(requests[r])
            selected_cs.append(cs)
            r+=1
        total_cost=0
        for cs_to_evaluate in csi:
            total_cost+=cs_to_evaluate.getNextCost()
            cs_to_evaluate.clear_window()
        #for to_reset in selected_cs:
            #total_cost+=csi[to_reset].getNextCost()
            #csi[to_reset].clear_window()
        #print c
        #print "COST:"+str(total_cost)
        if ref is None or check_float(total_cost ,ref)  < 0 :
            ref=total_cost
            result_candidate=c

    #print "RESULT ----> "+str(result_candidate)

    if result_candidate is not None:
        if requests[0]["time"]==0:
            csi[result_candidate[0].index(1)].addRequest(requests[0])
            #if result_candidate[0].index(1) >= (len(csi)-len(requests)):

            return csi[result_candidate[0].index(1)]
        else:
            return None
    else:
        return result_candidate


































def optimum_deploy(csi=[],requests=[],f=None):
    def check_float(a,b):
        if math.isclose(a,b):
            return 1
        else:
            return a-b

    cid = CSID()
    print ("Analyzing functionality: "+f)
    if len(requests) == 0:
        print  ("no request")
        return None


    for p_index in range(0,MAX_P+1):
        for k in range(0,2):
            csi_single=CloudService("f1",cid,"p1", p_index)
            csi.append(csi_single)



    print ("cutting...")
    deletere=[]
    r_index=0
    for r in requests:
        r_csi=0
        for c in csi:
            if c.check_deploy(r)==False:
              deletere.append([r_index,r_csi])
            r_csi+=1
        r_index+=1
    print("creating candidates...")
    candidate_matrix=partition_set_optimum(window=len(requests),matrix_d=len(csi),deleter=deletere,costant=len(requests))

    if len(requests) == 1:
        cc=[]
        for c in candidate_matrix:
           cc.append([c])
        candidate_matrix=cc

    candidate=candidate_matrix
    for cs in csi:
        cs.clear_window()
    ref=None
    result_candidate=None
    print ("Number of candidate:"+str(len(candidate)))
    for c in candidate:
        selected_cs=[]
        r=0
        for set_cs in c:
            cs = set_cs.index(1)
            csi[cs].add_request_window(requests[r])
            selected_cs.append(cs)
            r+=1
        total_cost=0
        app_refer=[]
        for cs_to_evaluate in csi:
            total_cost+=cs_to_evaluate.getNextCost()
            if len(cs_to_evaluate.window) > 0:
                app_refer.append(cs_to_evaluate)
            cs_to_evaluate.clear_window()

        if ref is None or check_float(total_cost ,ref)  < 0 :
            ref=total_cost
            result_candidate=app_refer

    #print "RESULT ----> "+str(result_candidate)
    print ("TOTAL COST"+str(ref))
    print (result_candidate)









def deploy_shift(csi,requests,f=None):
    def check_float(a,b):
        if math.isclose(a,b):
            return 1
        else:
            return a-b

    print ("Analyzing functionality: "+f)
    if len(requests) == 0:
        print  ("no request")
        return None

    deletere=[]
    r_index=0
    for r in requests:
        r_csi=0
        for c in csi:
            if c.check_deploy(r)==False:
              deletere.append([r_index,r_csi])
            r_csi+=1
        r_index+=1
    candidate_matrix=partition_set_smart(window=len(requests),matrix_d=len(csi),deleter=deletere)
    candidate=candidate_matrix
    if len(requests) == 1:
        cc=[]
        for c in candidate_matrix:
           cc.append([c])
        candidate_matrix=cc
    l_candidate = len(candidate_matrix)
    print ("Number of candidate tot:"+str(l_candidate))
    for cs in csi:
        cs.clear_window()
    ref=None
    result_candidate=None
    print ("Number of candidate:"+str(len(candidate)))
    #cutting branch
    for c in candidate:
        selected_cs=[]
        r=0
        for set_cs in c:
            cs = set_cs.index(1)
            csi[cs].add_request_window(requests[r])
            selected_cs.append(cs)
            r+=1
        total_cost=0
        for cs_to_evaluate in csi:
            total_cost+=cs_to_evaluate.getNextCost()
            cs_to_evaluate.clear_window()
        if ref is None or check_float(total_cost ,ref)  < 0 :
            ref=total_cost
            result_candidate=c

    if result_candidate is not None:
        rr=[]
        index_r = 0
        for set_cs in result_candidate:
            cs = set_cs.index(1)
            csi[cs].addRequest(requests[index_r])
            new=True
            for ci in rr:
                if ci.is_equal(csi[cs])==True:
                    new=False
                    break
            if new==True:
                rr.append(csi[cs])
            index_r=index_r+1
        return {"candidate":result_candidate,"result":rr}
    else:
        return None


















def iterative_optimim_deploy(csi,requests,f=None):


    print ("Analyzing functionality: "+f)
    if len(requests) == 0:
        print  ("no request")
        return None


#    candidate_matrix=partition_set_smart(window=len(requests),matrix_d=len(csi),deleter=deletere)

    deletere = []
    r_index = 0
    for r in requests:
        r_csi = 0
        for c in csi:
            if c.check_deploy(r) == False:
                deletere.append([r_index, r_csi])
            r_csi += 1
        r_index += 1


    column=len(csi)
    row=len(requests)
    matrix = [[0 for x in range(column)] for y in range(row)]
    for r in range(row):
        matrix[r][0] = 1
    #print(matrix)

    min_cost={"ref":None,"requests":requests,"csi":csi,"to_delete":deletere,"result_candidate":None}
    recursive(matrix,min_cost,0,row,column)
    print('\n\nRESULT:')
    print(min_cost["result_candidate"])
    print(min_cost["ref"])










    #if result_candidate is not None:
    #    if requests[0]["time"]==0:
    #        csi[result_candidate[0].index(1)].addRequest(requests[0])
    #        #if result_candidate[0].index(1) >= (len(csi)-len(requests)):
#
    #        return csi[result_candidate[0].index(1)]
    #    else:
    #        return None
    #else:
    #    return result_candidate
