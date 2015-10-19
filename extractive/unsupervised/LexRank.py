#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module LexRank
Please refer to the paper LexRank (Gunes Erkan and Dragomir R. Radev, 2009)
for more information
"""


__author__ = 'Lang-Chi Yu (yl871804@gmail.com)'
__license__ = 'Apache 2.0'
__version__ = '1.0.0'


import argparse
import math
from collections import Counter
from itertools import izip
from os import listdir, mkdir, path
from shutil import rmtree


def idf_modified_cosine(x, y, idf):
    tf_x = Counter(x)
    tf_y = Counter(y)
    tf_idf_x = [tf_x[w_x]*idf[w_x] for w_x in x]
    tf_idf_y = [tf_y[w_y]*idf[w_y] for w_y in y]
    numerator = sum([v*w for v, w in izip(tf_idf_x, tf_idf_y)])
    denominator = math.sqrt(sum([v**2 for v in tf_idf_x])*sum([w**2 for w in tf_idf_y]))
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0


def power_method(cosine_matrix, err_tolerance, damping_factor):
    N = len(cosine_matrix)
    p = [0]*N
    while True:
        p_new = [damping_factor*N]*N
        for i in range(N):
            for j in range(N):
                p_new[i] += (1-damping_factor) * cosine_matrix[i][j] * p[i]
        error = math.sqrt(sum([abs(a-b)**2 for a, b in izip(p, p_new)]))
        if error < err_tolerance:
            break
        p = p_new
    return p


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lorem Ipsum')
    parser.add_argument(
        "-I", "--input-dir", help="input files (folder)", required=True
    )
    parser.add_argument(
        "-O", "--output-dir", help="output folder", required=True
    )
    parser.add_argument(
        "-r", "--compression-rate",
        help="summary compression rate (default: 0.1)",
        type=float, default=0.1
    )
    parser.add_argument(
        "-th", "--cosine-threshold",
        help="similarity cosine threshold (default: 0.1)",
        type=float, default=0.1
    )
    parser.add_argument(
        "-tol", "--err-tolerance",
        help="power method convergence metric (default: 1e-4)",
        type=float, default=1e-4
    )
    parser.add_argument(
        "-d", "--damping-factor",
        help="damping factor in PageRank Algorithm (default: 0.15)",
        type=float, default=0.15
    )
    parser.add_argument(
        "-c", "--continuous",
        help="Continuous LexRank (default=False)",
        action="store_true", dest="continuous", default=False
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    compression_rate = args.compression_rate
    cosine_threshold = args.cosine_threshold
    err_tolerance = args.err_tolerance
    damping_factor = args.damping_factor
    continuous = args.continuous

    if path.exists(output_dir):
        rmtree(output_dir)
    mkdir(output_dir)

    docs = {}
    idf = {}
    for f in listdir(input_dir):
        with open(path.join(input_dir, f), 'r') as fin:
            doc = []
            idf_doc = {}
            for line in fin:
                words = line.rstrip().split()
                if len(words) != 0:
                    doc.append(words)
                    for word in words:
                        idf_doc[word] = 1

            docs[f] = doc
            for word in idf_doc:
                if word not in idf:
                    idf[word] = 1
                else:
                    idf[word] += 1

    for f, doc in docs.iteritems():
        print f
        n = len(doc)
        cosine_matrix = []
        for _ in range(n):
            cosine_matrix.append([0]*n)
        degree = [0]*n

        for i in range(n):
            for j in range(n):
                sent_i = doc[i]
                sent_j = doc[j]
                cos = idf_modified_cosine(sent_i, sent_j, idf)
                if cos > cosine_threshold:
                    if not continuous:
                        cos = 1

                    cosine_matrix[i][j] = cos
                    degree[i] += cos

        for i in range(n):
            for j in range(n):
                cosine_matrix[i][j] /= float(degree[i])

        L = power_method(cosine_matrix, err_tolerance, damping_factor)
        with open(path.join(output_dir, f), 'w') as fout:
            score_order = [s[0] for s in sorted(
                enumerate(L), key=lambda x: x[1], reverse=True
            )]
            summ_len = int(compression_rate*len(doc))
            candidates = score_order[:summ_len]
            for cand_id in candidates:
                candidate = doc[cand_id]
                for word in candidate:
                    fout.write(word)
                    fout.write(" ")
                fout.write("\n")
