# -*- coding: UTF-8 -*-

import re
import sys
import time
import datetime
import math
from collections import Counter

# reload(sys)
# sys.setdefaultencoding('utf-8')

# K = int(sys.argv[1])
# M_num = int(sys.argv[2])
K = 20
M_num = 10


def coherence(filename1="../output/model/k%d.pw_z" % K, filename2="../output/doc_wids.txt", M=M_num, e=pow(10, -6),
              K_num=K):
    file1 = open(filename1)
    file2 = open(filename2)
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
            if (len(list_M_pro) < M):
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
        for i in range(M):
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


if __name__ == "__main__":
    coherence()
