import copy
def WAND_Algo(query_terms, top_k, inverted_index):

    query_list = []
    for k in query_terms:
        temp_d = {}
        temp_d['term'] = k
        temp_d['docID']=[]
        temp_d['w'] = []
        temp_d['lastID'] = False
        for docid,w in inverted_index[k]:
            temp_d['docID'].append(docid)
            temp_d['curDoc'] = 0
            temp_d['w'].append(w)
            temp_d['dID'] = temp_d['docID'][temp_d['curDoc']]
        query_list.append(temp_d)

    theta = float('-inf')
    Topk = []
    Evaluation_Count = 0

    while query_list != []:
        query_list = sorted(query_list, key=lambda d: d['dID'])
        copy_query_list = copy.deepcopy(query_list)
        UB_list = []
        for d in query_list:
            UB_list.append(max(d['w']))
        score_limit = 0
        pivot = 0
        while pivot < len(query_list):
            tmp_s_lim = score_limit + UB_list[pivot]
            if tmp_s_lim > theta:
                break
            score_limit = tmp_s_lim
            pivot+=1
        # if score_limit<=theta:
        #     break
        if pivot>len(copy_query_list)-1:
            break
        if copy_query_list[0]['dID'] == copy_query_list[pivot]['dID']:
            Evaluation_Count += 1
            s = 0
            t = 0
            while t < len(copy_query_list) and copy_query_list[t]['dID'] == copy_query_list[pivot]['dID']:
                s += copy_query_list[t]['w'][copy_query_list[t]['curDoc']]
                query_list[t]['curDoc'] += 1
                if query_list[t]['curDoc']<=len(query_list[t]['docID'])-1:
                    query_list[t]['dID'] = query_list[t]['docID'][query_list[t]['curDoc']]


                else:
                    query_list[t]['lastID'] = True
                t = t + 1


            if s > theta:
                Topk.append((s,copy_query_list[pivot]['dID']))

                if len(Topk)>top_k:
                    Topk = sorted(Topk, key=lambda x:(x[0],-x[1]))
                    Topk.pop(0)
                    theta = Topk[0][0]
            del_list = []
            for d1 in query_list:
                if d1['lastID'] == True:
                    del_list.append(d1)
            if del_list:
                for d2 in del_list:
                    query_list.remove(d2)

        else:
            for i in range(0,pivot):
                while query_list[i]['dID'] < query_list[pivot]['dID'] and query_list[i]['lastID'] != True:
                    query_list[i]['curDoc'] += 1
                    if query_list[i]['curDoc'] <= len(query_list[i]['docID']) - 1:
                        query_list[i]['dID'] = query_list[i]['docID'][query_list[i]['curDoc']]

                    else:
                        query_list[i]['lastID'] = True

            del_list = []
            for d1 in query_list:
                if d1['lastID'] == True:
                    del_list.append(d1)
            if del_list:
                for d2 in del_list:
                    query_list.remove(d2)

    return sorted(Topk, key=lambda x:(-x[0],x[1])),Evaluation_Count







