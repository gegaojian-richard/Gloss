#!/usr/bin/env python3
# coding=utf-8
# Function: 训练word2vec模型


import sys
from gensim.models import word2vec
from gensim.models import KeyedVectors
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def build_word2vec_model(source_file, model_file, a_size, a_window, a_alpha, a_workers, a_min_count, a_iter, a_hs,
                         a_sg):
    # sentences = word2vec.Text8Corpus(source_file)
    sentences = [doc.strip().split() for doc in open(source_file, encoding='utf-8').readlines()]
    model = word2vec.Word2Vec(sentences, size=a_size, window=a_window, alpha=a_alpha, workers=a_workers,
                              min_count=a_min_count, iter=a_iter, hs=a_hs, sg=a_sg)
    model.wv.save_word2vec_format(model_file, binary=True)
    return model.wv


def get_word2vec_model(filename):
    return KeyedVectors.load_word2vec_format(filename, binary=True)


if __name__ == '__main__':
    if len(sys.argv) < 11:
        print(
            'Usage: python3 %s <w2v_corpus_pt> <w2v_model_pt> <w2v_size> <w2v_window> <w2v_alpha> <w2v_workers> <w2v_min_count> <w2v_iter> <w2v_hs> <w2v_sg>' %
            sys.argv[0])
        print('\tw2v_corpus_pt    the corpus to train word2vec model')
        print('\tw2v_model_pt    the word2vec model file')
        print('\tw2v_size    the word2vec size')
        print('\tw2v_window    the word2vec window')
        print('\tw2v_alpha    the word2vec aplha')
        print('\tw2v_workers    the word2vec workers')
        print('\tw2v_min_count    the word2vec min_count')
        print('\tw2v_iter    the word2vec iter')
        print('\tw2v_hs    the word2vec hs')
        print('\tw2v_sg    the word2vec sg')
        exit(1)

    w2v_corpus_pt = sys.argv[1]
    w2v_model_pt = sys.argv[2]
    w2v_size = int(sys.argv[3])
    w2v_window = int(sys.argv[4])
    w2v_alpha = float(sys.argv[5])
    w2v_workers = int(sys.argv[6])
    w2v_min_count = int(sys.argv[7])
    w2v_iter = int(sys.argv[8])
    w2v_hs = int(sys.argv[9])
    w2v_sg = int(sys.argv[10])
    build_word2vec_model(w2v_corpus_pt, w2v_model_pt, w2v_size, w2v_window, w2v_alpha, w2v_workers, w2v_min_count,
                         w2v_iter, w2v_hs, w2v_sg)
