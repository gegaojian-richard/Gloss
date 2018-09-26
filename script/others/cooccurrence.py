#!/usr/bin/env python3
# coding=utf-8
# Function: compute co-occurrence of a pair of words in corpus by doc

import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def cooccurrence(corpus_pt, word1, word2):
    logger.info("Compute co-occurrence of " + word1 + " and " + word2 + " in : " + corpus_pt)
    doc_list = open(corpus_pt, encoding='utf-8').readlines()
    count = 0
    for doc in doc_list:
        words_set_in_doc = set([word for word in doc.strip().split()])
        if word1 in words_set_in_doc and word2 in words_set_in_doc:
            count += 1
            logger.info("Find in doc : " + doc.strip())

    logger.info("co-occurrence of " + word1 + " and " + word2 + " : " + str(count))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 %s <corpus_pt> <word1> <word2>' % sys.argv[0])
        exit(1)

    corpus_pt = sys.argv[1]
    word1 = sys.argv[2]
    word2 = sys.argv[3]

    cooccurrence(corpus_pt, word1, word2)