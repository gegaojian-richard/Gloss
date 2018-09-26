#!/usr/bin/env python3
# coding=utf-8
# Function: scores


import sys
import math
import numpy

def _mean(filename):
    scores_file = open(filename, mode='r', encoding='utf-8')
    scores = [float(score.strip()) for score in scores_file.readlines() if score.strip() != ""]
    array_scores = numpy.array(scores).astype(numpy.float)
    mean_scores = array_scores.mean()
    std_scores = array_scores.std()/math.sqrt(10)
    scores_file.close()
    scores_file = open(filename, mode='a', encoding='utf-8')
    scores_file.write("\n")
    scores_file.write(str(mean_scores) + "+-" + str(std_scores))
    scores_file.close()

def mean(output_dir):
    _mean(output_dir + "RandomForest_Accuracies.txt")
    _mean(output_dir + "NB_Accuracies.txt")
    _mean(output_dir + "K-means_Homogeneities.txt")
    _mean(output_dir + "K-means_V-measures.txt")
    _mean(output_dir + "Coherence5.txt")
    _mean(output_dir + "Coherence10.txt")
    _mean(output_dir + "Coherence20.txt")
    _mean(output_dir + "Purityies.txt")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 %s <output_dir>' % sys.argv[0])
        exit(1)

    output_dir = sys.argv[1]

    mean(output_dir)