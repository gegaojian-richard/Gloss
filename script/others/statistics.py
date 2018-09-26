#!/usr/bin/env python3
# coding=utf-8
# Function: compute co-occurrence of a pair of words in corpus by doc

import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def statistics(corpus_pt, label_pt):
    logger.info("Statistics of Corpus : " + corpus_pt)
    doc_list = open(corpus_pt, encoding='utf-8').readlines()
    label_list = open(label_pt, encoding='utf-8').readlines()
    category_count = len(list(set(label_list)))
    doc_count = len(doc_list)
    logger.info("Count of Categories : " + str(category_count))
    logger.info("Count of Documents : " + str(doc_count))
    all_words_list = [word for doc in doc_list for word in doc.strip().split()]
    all_words_count = len(all_words_list)
    voca_list = list(set(all_words_list))
    voca_len = len(voca_list)
    logger.info("Count of words per document : " + str(all_words_count/doc_count))
    logger.info("Length fo Vocabulary : " + str(voca_len))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 %s <corpus_pt> <label_pt>' % sys.argv[0])
        exit(1)

    corpus_pt = sys.argv[1]
    label_pt = sys.argv[2]

    statistics(corpus_pt, label_pt)