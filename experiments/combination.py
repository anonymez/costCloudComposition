from collections import deque
import math
import itertools


def calculate_cost(matrix):
    for row in matrix:
         bucket=row.index(1)

def full_rotation(matrix,min_cost):
        r=len(matrix)-1
        column=len(matrix[r])
        #print("------")
        for c in range(column):
            to_rotate = deque(matrix[r])
            to_rotate.rotate(1)
            matrix[r] = list(to_rotate)
            #print (matrix)
            to_delete=min_cost["to_delete"]
            csi=min_cost["csi"]
            requests=min_cost["requests"]

            if [r,matrix[r].index(1)] in to_delete:
                #print ("not compatible")
                pass
            else:
                for cs in csi:
                    cs.clear_window()
                ref = min_cost["ref"]
                selected_cs = []
                r_index = 0
                for set_cs in matrix:
                    cs = set_cs.index(1)
                    csi[cs].add_request_window(requests[r_index])
                    selected_cs.append(cs)
                    r_index += 1
                total_cost = 0
                for cs_to_evaluate in csi:
                    total_cost += cs_to_evaluate.getNextCost()
                    cs_to_evaluate.clear_window()
                if min_cost["ref"] is None or check_float(total_cost, min_cost["ref"]) < 0:
                    min_cost["ref"] = total_cost
                    min_cost["result_candidate"]=str(matrix)







            #cost=calculate_cost(matrix)
            #if check_float(cost,min_cost)<0:
            #    min_cost=cost
            #print ("Matrix")
            #for r in range(row):
            #    print (matrix[r])

def check_float(a,b):
    if math.isclose(a,b):
        return 0
    else:
        return a-b

def recursive(matrix,min_cost,row,tot_row,tot_column):
    if (row==tot_row-1):
        full_rotation(matrix,min_cost)
        to_rotate = deque(matrix[row])
        to_rotate.rotate(1)
        matrix[row] = list(to_rotate)
    else:
        for index in range(tot_column):
            if [row,matrix[row].index(1)] in min_cost["to_delete"]:
                #print ("not compatible")
                pass
            else:
                recursive(matrix,min_cost,row+1,tot_row,tot_column)
            to_rotate = deque(matrix[row])
            to_rotate.rotate(1)
            matrix[row] = list(to_rotate)








    #for a in range(column):
    #    for b in range(column):
    #        for c in range(column):
    #            for d in range(column):
    #                for e in range(column):
    #                    for f in range(column):
    #                        for g in range(column):
    #                            full_rotation(matrix)
    #                            to_rotate = deque(matrix[6])
    #                            to_rotate.rotate(1)
    #                            matrix[6] = list(to_rotate)
    #                        to_rotate = deque(matrix[5])
    #                        to_rotate.rotate(1)
    #                        matrix[5] = list(to_rotate)
    #                    to_rotate = deque(matrix[4])
    #                    to_rotate.rotate(1)
    #                    matrix[4] = list(to_rotate)
    #                to_rotate = deque(matrix[3])
    #                to_rotate.rotate(1)
    #                matrix[3] = list(to_rotate)
    #            to_rotate = deque(matrix[2])
    #            to_rotate.rotate(1)
    #            matrix[2] = list(to_rotate)
    #        to_rotate = deque(matrix[1])
    #        to_rotate.rotate(1)
    #        matrix[1] = list(to_rotate)
    #    to_rotate = deque(matrix[0])
    #    to_rotate.rotate(1)
    #    matrix[0] = list(to_rotate)




                #shit 1
            #shif 1
        #shift 1


