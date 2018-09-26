#!/usr/bin/env python3
# coding=utf-8
# Function: 将训练语料Corpus合并到text8中


import sys
from progressbar import ProgressBar,Bar,Percentage
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def merge_corpus2text8(corpuspath, text8path):
    logger.info('将语料 - ' + corpuspath + ' 添加到' + text8path + '中...')
    doc_list = open(corpuspath, encoding='utf-8').readlines()
    doc_count = len(doc_list)
    logger.info("Count of corpus - " + corpuspath + " : " + str(doc_count))
    train_text = open(text8path, mode='a', encoding='utf-8')
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=doc_count).start()
    for i in range(doc_count):
        train_text.write(doc_list[i].strip() + " ")
        pbar.update(i + 1)
    pbar.finish()

    train_text.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 %s <corpus_pt> <text8_pt>' % sys.argv[0])
        print('\tcorpus_pt    the origin corpus')
        print('\ttext8_pt    the origin text8 file')
        exit(1)

    corpus_pt = sys.argv[1]
    text8_pt = sys.argv[2]
    merge_corpus2text8(corpus_pt, text8_pt)
