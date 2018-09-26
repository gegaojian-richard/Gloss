#!/usr/bin/env python3
# coding=utf-8
# Function: 将训练语料Corpus合并到text8中


import sys
import math
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.cluster import KMeans
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def add_two_dim_dict(thedict, key1, key2, val):
    if (key1 in thedict):
        thedict[key1].update({key2: val})
    else:
        thedict.update({key1: {key2: val}})


def purity(label_pt, btm_pzd_pt, M=22,
           N=20):  # filename2中的参数是可以调整的
    file1 = open(label_pt)
    file2 = open(btm_pzd_pt)
    i = 0
    n = 0
    dict_doc_cluster = {}
    list_type = []
    for line1 in file1:
        i += 1
        split = line1.replace("\n", "")
        dict_doc_cluster[i] = split
    i = 0
    N = 0
    split_pro = {}
    split_index = {}
    for line2 in file2:
        # split = line2.replace("\n", "").split(" ")
        split = line2.strip().split()
        i += 1
        split_pro[i] = 0
        split_index[i] = 0
        for j in range(len(split)):
            # print float(split[j])
            # if ((split[j] == '') or (split[j] == '\n')):
            #     continue
            if (split_pro[i] < float(split[j])):
                split_pro[i] = float(split[j])
                split_index[i] = j
        n += 1
    # print n
    dict_cluster = {}
    for i in range(1, n + 1):
        a = split_index[i]  # a是每个文档对应的最大概率的主题
        b = dict_doc_cluster[i]  # b是每个文档实际的类标
        # print a,b
        if (a in dict_cluster):
            if (b in dict_cluster[a]):
                dict_cluster[a][b] += 1
                N += 1
            else:
                add_two_dim_dict(dict_cluster, a, b, 1)
                N += 1
        else:
            add_two_dim_dict(dict_cluster, a, b, 1)
            N += 1
    # print N
    dict_sum = 0
    # print len(dict_cluster)
    for i in dict_cluster:
        # print i
        dict_max = 0
        s = 0
        for j in dict_cluster[i]:
            if (dict_max == 0):
                dict_max = dict_cluster[i][j]
                s += dict_cluster[i][j]
            else:
                if (dict_max < dict_cluster[i][j]):
                    dict_max = dict_cluster[i][j]
                s += dict_cluster[i][j]
        # print i,dict_max,s
        dict_sum += dict_max
    # print((dict_sum + 0.0) / N)
    return (dict_sum + 0.0) / N


def coherence(btm_pwz_pt, dwid_pt, coherence_M, e=pow(10, -6),
              K_num=20):
    file1 = open(btm_pwz_pt)
    file2 = open(dwid_pt)
    list_doc_wids = []
    average = 0
    count = 1
    for line2 in file2:
        split = line2.replace("\n", "").split(" ")
        count = count + 1
        for i in range(len(split)):
            if (split[i] != ''):
                # print split[i]
                split[i] = int(split[i])
        list_doc_wids.append(split)
    # print list_doc_wids
    count = 0
    for line1 in file1:
        count += 1
        split = line1.replace("\n", "").split(" ")
        length = len(split)
        list_M_index = []
        list_M_pro = []
        for i in range(length - 1):
            if (len(list_M_pro) < coherence_M):
                list_M_index.append(i)
                list_M_pro.append(float(split[i]))
            else:
                if (min(list_M_pro) < float(split[i])):
                    j = list_M_pro.index(min(list_M_pro))
                    list_M_index[j] = i
                    list_M_pro[j] = float(split[i])
        for i in range(len(list_M_pro)):
            for j in range(i + 1, len(list_M_pro)):
                if (list_M_pro[i] < list_M_pro[j]):
                    temp = list_M_pro[i]
                    list_M_pro[i] = list_M_pro[j]
                    list_M_pro[j] = temp
                    temp = list_M_index[i]
                    list_M_index[i] = list_M_index[j]
                    list_M_index[j] = temp
        '''
        for i in range(M):
			print list_M_index[i],list_M_pro[i]  
        break    
        '''
        # print list_M_index
        result = 0
        for i in range(coherence_M):
            for j in range(i):
                # print i,j

                index_i = list_M_index[i]
                index_j = list_M_index[j]
                num_i_and_j = 0
                num_j = 0
                for l in list_doc_wids:
                    # print index_i,index_j,l
                    if (index_j in l):
                        num_j += 1
                        # print"j"
                    if ((index_i in l) and (index_j in l)):
                        num_i_and_j += 1
                        # print"i"
                # print num_i_and_j,num_j,(num_i_and_j+e)/num_j
                result += math.log10((num_i_and_j + e) / num_j)
                '''
                if (num_i_and_j == 0):
                    print count,':',index_i, ',', index_j, ' ', num_i_and_j, ' ', math.log10((num_i_and_j+e)/num_j)
                '''
        # print result
        average += result
    average = average / K_num
    # print (average)
    file1.close()
    file2.close()
    return average


def scores(btm_pzd_pt, btm_pwz_pt, dwid_pt, label_pt, btm_K, output_dir):
    feature_file = open(btm_pzd_pt, 'r')
    label_file = open(label_pt, 'r')
    feature_matrix = [[float(feature) for feature in doc.split()] for doc in feature_file.readlines()]
    label_list = []
    dict_label = {}

    for line in label_file.readlines():
        label = line.split('&')[0].strip()

        if label not in dict_label:
            dict_label[label] = len(dict_label)

        label_list.append(dict_label[label])

    feature_file.close()
    label_file.close()

    X_train, X_test, y_train, y_test = train_test_split(np.array(feature_matrix), np.array(label_list), test_size=0.2,
                                                        random_state=0)

    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(X_train, y_train)
    rfa = str(clf.score(X_test, y_test))
    logger.info("RandomForest Accuracy : " + rfa)

    gnb = GaussianNB()
    gnb = gnb.fit(X_train, y_train)
    nba = str(gnb.score(X_test, y_test))
    logger.info("NB Accuracy : " + nba)

    km = KMeans(n_clusters=30, init='k-means++', max_iter=100, n_init=1,
                verbose=False)

    km.fit(feature_matrix)
    kh = str(metrics.homogeneity_score(label_list, km.labels_))
    kv = str(metrics.v_measure_score(label_list, km.labels_))
    logger.info("K-means Homogeneity : " + kh)
    logger.info("K-means V-measure : " + kv)

    c5 = str(coherence(btm_pwz_pt, dwid_pt, 5, e=pow(10, -6), K_num=btm_K))
    c10 = str(coherence(btm_pwz_pt, dwid_pt, 10, e=pow(10, -6), K_num=btm_K))
    c20 = str(coherence(btm_pwz_pt, dwid_pt, 20, e=pow(10, -6), K_num=btm_K))
    p_m = str(purity(label_pt, btm_pzd_pt))
    logger.info("Coherence : " + c5)
    logger.info("Coherence : " + c10)
    logger.info("Coherence : " + c20)
    logger.info("Purity : " + p_m)
    rfa_file = open(file=output_dir + "RandomForest_Accuracies.txt", mode='a', encoding='utf-8')
    rfa_file.write("\n")
    rfa_file.write(rfa)
    rfa_file.close()
    nba_file = open(file=output_dir + "NB_Accuracies.txt", mode='a', encoding='utf-8')
    nba_file.write("\n")
    nba_file.write(nba)
    nba_file.close()
    kh_file = open(file=output_dir + "K-means_Homogeneities.txt", mode='a', encoding='utf-8')
    kh_file.write("\n")
    kh_file.write(kh)
    kh_file.close()
    kv_file = open(file=output_dir + "K-means_V-measures.txt", mode='a', encoding='utf-8')
    kv_file.write("\n")
    kv_file.write(kv)
    kv_file.close()
    c5_file = open(file=output_dir + "Coherence5.txt", mode='a', encoding='utf-8')
    c5_file.write("\n")
    c5_file.write(c5)
    c5_file.close()
    c10_file = open(file=output_dir + "Coherence10.txt", mode='a', encoding='utf-8')
    c10_file.write("\n")
    c10_file.write(c10)
    c10_file.close()
    c20_file = open(file=output_dir + "Coherence20.txt", mode='a', encoding='utf-8')
    c20_file.write("\n")
    c20_file.write(c20)
    c20_file.close()
    p_file = open(file=output_dir + "Purityies.txt", mode='a', encoding='utf-8')
    p_file.write("\n")
    p_file.write(p_m)
    p_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('Usage: python3 %s <btm_pzd_pt> <btm_pwz_pt> <dwid_pt> <label_pt> <btm_K> <output_dir>' % sys.argv[0])
        exit(1)

    btm_pzd_pt = sys.argv[1]
    btm_pwz_pt = sys.argv[2]
    dwid_pt = sys.argv[3]
    label_pt = sys.argv[4]
    btm_K = int(sys.argv[5])
    output_dir = sys.argv[6]

    scores(btm_pzd_pt, btm_pwz_pt, dwid_pt, label_pt, btm_K, output_dir)
