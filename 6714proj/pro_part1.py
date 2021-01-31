import copy
def WAND_Algo(query_terms, top_k, inverted_index):
    query_list = []
    for k in query_terms:
        temp_l = []
        temp_l.append([k])#store the name of term 0
        temp_l.append([])#docID list of term 1
        temp_l.append([])#socre list of term 2
        temp_l.append([0])#curDoc cursor      3
        temp_l.append([])#cueDoc ID          4
        temp_l.append([False])#if cursor move to last, then True 5
        for docid,w in inverted_index[k]:
            temp_l[1].append(docid)
            temp_l[2].append(w)
            temp_l[4] = [temp_l[1][temp_l[3][-1]]]
        query_list.append(temp_l)

    theta = float('-inf')
    Topk = []
    Evaluation_Count = 0

    while query_list != []:
        query_list = sorted(query_list, key=lambda d: d[4][-1])
        copy_query_list = copy.deepcopy(query_list)
        UB_list = []
        for d in query_list:
            UB_list.append(max(d[2]))
        score_limit = 0
        pivot = 0
        while pivot < len(query_list):
            tmp_s_lim = score_limit + UB_list[pivot]
            if tmp_s_lim > theta:
                break
            score_limit = tmp_s_lim
            pivot += 1
        # if score_limit<=theta:
        #     break
        if pivot>len(copy_query_list)-1:
            break
        if copy_query_list[0][4][-1] == copy_query_list[pivot][4][-1]:
            Evaluation_Count += 1
            s = 0
            t = 0
            while t < len(copy_query_list) and copy_query_list[t][4][-1] == copy_query_list[pivot][4][-1]:
                s += copy_query_list[t][2][copy_query_list[t][3][-1]]
                query_list[t][3][-1] += 1
                if query_list[t][3][-1]<=len(query_list[t][1])-1:
                    query_list[t][4][-1] = query_list[t][1][query_list[t][3][-1]]


                else:
                    query_list[t][5][-1] = True
                t = t + 1

            if s > theta:
                Topk.append((s,copy_query_list[pivot][4][-1]))

                if len(Topk)>top_k:
                    Topk = sorted(Topk, key=lambda x:(x[0],-x[1]))
                    Topk.pop(0)
                    theta = Topk[0][0]
            del_list = []
            for d1 in query_list:
                if d1[5][-1] == True:
                    del_list.append(d1)
            if del_list:
                for d2 in del_list:
                    query_list.remove(d2)
        else:
            for i in range(0,pivot):
                while query_list[i][4][-1] < query_list[pivot][4][-1] and query_list[i][5][-1] != True:
                    query_list[i][3][-1] += 1
                    if query_list[i][3][-1] <= len(query_list[i][1]) - 1:
                        query_list[i][4][-1] = query_list[i][1][query_list[i][3][-1]]

                    else:
                        query_list[i][5][-1] = True

            del_list = []
            for d1 in query_list:
                if d1[5][-1] == True:
                    del_list.append(d1)
            if del_list:
                for d2 in del_list:
                    query_list.remove(d2)

    return sorted(Topk, key=lambda x: (-x[0], x[1])), Evaluation_Count