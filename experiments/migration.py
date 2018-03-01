from experiments.deployer import  check_float

def migrate(pivot,csi):
    candidate=[]
    print ("migration start")
    #1st phase
    requests=[]
    for ci in csi:
        for r in ci.requests:
            requests.append({"request":r,"csi":ci})
    requests.sort(key=lambda x: x["request"]["p"]["level"], reverse=True)
    for r in requests:
        if (r["request"]["p"]["level"] <= pivot.property.level):
            print ("possibile migration of "+str(r))
            if check_migration(r,pivot):
                print ("\n\n "+str(r) +" is migrated from "+str(r["csi"].get_id())+ " to "+str(pivot.get_id()))
                new=True
                for cc in candidate:
                    if cc.get_id()==r["csi"].get_id():
                        new=False
                        break
                if new == True:
                    candidate.append(r["csi"])
    #2nd phase
    if len(candidate)>1:
        for c in candidate:
            print ("candidate to join "+str(c.get_id()))
        candidate_couple=[]
        while True:
            ref=None
            for c1 in range(0,len(candidate)):
                for c2 in range(0,len(candidate)):
                    if c1!=c2 and candidate[c1].property.level>=candidate[c2].property.level:
                        #candidate[c1].clear_window()
                        candidate[c1].add_requests_window(candidate[c2].requests)
                        new_cost=candidate[c1].getNextCost()
                        delta=new_cost-(candidate[c2].get_total_cost()+candidate[c1].get_total_cost())
                        if delta<0:
                            couple={"couple":[candidate[c1],candidate[c2]],"delta_cost":delta}
                            candidate_couple.append(couple)
                            if ref==None or check_float(delta,ref["delta_cost"])>0:
                                ref=couple
            if ref == None:
                break
            to_delete=[]
            for cc in range(0, len(candidate)):
                if candidate[cc] in ref["couple"]:
                    to_delete.append(cc)
            app_candidate = [i for j, i in enumerate(candidate) if j not in to_delete]
            print ("2nd Phase Migration")
            candidate=app_candidate
            if len(candidate)==1 or ref == None:
                break





def check_migration(request,ci):
    request["csi"].clear_window()
    request["csi"].add_request_window(request["request"])
    delta_down = request["csi"].get_total_cost()-request["csi"].window_delete()
    ci.clear_window()
    ci.add_request_window(request["request"])
    delta_up = ci.get_window_cost()
    mmi=check_float(delta_up, delta_down)
    print ("mmi="+str(mmi))
    if mmi<0:
        request["csi"].delete(request["request"])
        ci.addRequest(request["request"])
        return True
    else:
        return False

