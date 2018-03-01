from collections import deque
from window import WINDOW


def partition_set(window,matrix_d):
    nitem=window
    k=matrix_d
    if nitem == 0:
        return None
    dist_list=[0]*k;
    dist_list[0]=1
    dist=deque(dist_list)
    result=[]
    for shift in range(0,k):
        source=list(dist)
        mat = partition_set(nitem-1,k)
        if (k == 5):
            print("hello")
        if mat is not None:
            for r in mat:
                app = []
                if isinstance(r[0], list)== False:
                    r=[r]
                app=[source]+r
                result.append(app)
        else:
            result.append(source)
        dist.rotate(1)
    return result


def partition_set_smart(window,matrix_d,deleter):
    nitem=window
    k=matrix_d
    if nitem == 0:
        return None
    dist_list=[0]*k;
    dist_list[0]=1
    dist=deque(dist_list)
    result=[]
    for shift in range(0,k):
        if [WINDOW-window,shift] in deleter:
            pass
        else:
            #return False
            source=list(dist)
            mat = partition_set_smart(nitem-1,k,deleter)

            if mat is not None:
                for r in mat:
                    app = []
                    if isinstance(r[0], list)== False:
                        r=[r]
                    app=[source]+r
                    result.append(app)
            else:
                result.append(source)
        dist.rotate(1)
    return result

def partition_set_optimum(window, matrix_d, deleter,costant):
    nitem = window
    k = matrix_d
    if nitem == 0:
        return None
    dist_list = [0] * k;
    dist_list[0] = 1
    dist = deque(dist_list)
    result = []
    for shift in range(0, k):
        if [costant - window, shift] in deleter:
            pass
        else:
            # return False
            source = list(dist)
            mat = partition_set_optimum(nitem - 1, k, deleter,costant)
            if mat is not None:
                for r in mat:
                    app = []
                    if isinstance(r[0], list) == False:
                        r = [r]
                    app = [source] + r
                    result.append(app)
            else:
                result.append(source)
        dist.rotate(1)
    return result

def partition_iterator(window, matrix_d ):
    nitem = window
    k = matrix_d
    if nitem == 0:
        return None

    for block in range (0,window):
        dist_list = [0] * k;
        dist_list[0] = 1
        dist = deque(dist_list)
        repetition=matrix_d**block
        appendix=[]
        for c in range(0,matrix_d):
            source = list(dist)
            for row in range(0,repetition):
                appendix.append([source.index(1)])
            dist.rotate(1)
            #print (appendix)
        print ("new block ------")







#a = partition_set_smart(2,3,[[0,1]])
#a = partition_iterator(20,6)

#for to_print in a:
#    print (to_print)