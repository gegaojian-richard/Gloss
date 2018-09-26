#!/usr/bin/env python3
# coding=utf-8
# Function: 训练word2vec模型


import sys
from gensim.models import KeyedVectors
from progressbar import ProgressBar, Bar, Percentage
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def map2index(w2v_model_pt, voca_pt, ntop, threshold, wm_pt, mw_pt):
    logger.info("1. 读取单词表")
    voca_dict = {}
    word_list = []
    for line in open(voca_pt, encoding='utf-8').readlines():
        temp = line.strip().split()
        voca_dict[temp[1]] = temp[0]
        word_list.append(temp[1])
    word_set = set(word_list)

    logger.info("2. 读取word2vec模型")
    word_vector = KeyedVectors.load_word2vec_format(w2v_model_pt, binary=True)

    # 思路：
    # 1) 判断word是否在maped_words集合中
    # 2）若没有，则根据word2vec计算word的merged_num个语义相近词，语义相近的最低阀值为threshold
    # 3）若有，则跳过
    mapped_words = set()
    word_map = {}  # word-word
    word_dict = {}  # word-words
    score_map = {}  # word - similarity
    key_set = set()

    logger.info("3. 生成单词映射表")
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(word_list)).start()
    for i in range(len(word_list)):
        if word_list[i] not in mapped_words:
            mapped_words.add(word_list[i])
            word_dict[word_list[i]] = []
            candidates = [candidate for candidate in word_vector.most_similar(word_list[i], topn=50) if
                          candidate[1] > threshold]
            synonyms = []
            for j in range(len(candidates)):
                if candidates[j][0] not in word_set:
                    continue
                if candidates[j][0] in key_set:
                    continue
                if candidates[j][0] in mapped_words:
                    if score_map[candidates[j][0]] < candidates[j][1]:
                        word_dict[word_map[candidates[j][0]]] = [word for word in word_dict[word_map[candidates[j][0]]]
                                                                 if word != candidates[j][0]]
                    else:
                        continue
                synonyms.append(candidates[j])
                if len(synonyms) == ntop:
                    break
            for j in range(len(synonyms)):
                mapped_words.add(synonyms[j][0])
                word_map[synonyms[j][0]] = word_list[i]
                score_map[synonyms[j][0]] = synonyms[j][1]
                word_dict[word_list[i]].append(synonyms[j][0])
            key_set.add(word_list[i])
        pbar.update(i + 1)
    pbar.finish()
    logger.info('4. 保存单词映射表')
    words_map_file = open(file=wm_pt,
                          mode='w', encoding='utf-8')
    mapped_wids_file = open(file=mw_pt,
                          mode='w', encoding='utf-8')
    for key in word_dict.keys():
        line = key + " : "
        line += ' '.join(word_dict[key])
        words_map_file.write(line + '\n')
        line = voca_dict[key] + " "
        line += ' '.join(voca_dict[word] for word in word_dict[key])
        mapped_wids_file.write(line + '\n')
    words_map_file.close()
    mapped_wids_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print(
            'Usage: python3 %s <w2v_model_pt> <voca_pt> <ntop> <threshold> <wm_pt> <mw_pt>' %
            sys.argv[0])
        print('\tw2v_model_pt    the word2vec model file')
        print('\tvoca_pt    the voca file')
        print('\tntop    the ntop')
        print('\tthreshold    the threshold')
        print('\twm_pt    the words map file')
        print('\tmw_pt    the mapped wids file')
        exit(1)

    w2v_model_pt = sys.argv[1]
    voca_pt = sys.argv[2]
    ntop = int(sys.argv[3])
    threshold = float(sys.argv[4])
    wm_pt = sys.argv[5]
    mw_pt = sys.argv[6]

    map2index(w2v_model_pt, voca_pt, ntop, threshold, wm_pt, mw_pt)
