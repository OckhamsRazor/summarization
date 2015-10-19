#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module Centrality
Please refer to the paper LexRank (Gunes Erkan and Dragomir R. Radev, 2009)
for more information
"""


__author__ = 'Lang-Chi Yu (yl871804@gmail.com)'
__license__ = 'Apache 2.0'
__version__ = '1.0.0'


import argparse
import math
from os import listdir, mkdir, path
from shutil import rmtree


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
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    compression_rate = args.compression_rate
    cosine_threshold = args.cosine_threshold

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
        word_hash = {}
        c = []
        for sent in doc:
            for word in sent:
                if word not in word_hash:
                    word_hash[word] = idf[word]
                else:
                    word_hash[word] += idf[word]

        for sent in doc:
            score = 0
            for word in sent:
                if word_hash[word] > cosine_threshold:
                    score += word_hash[word]
            c.append(score)

        with open(path.join(output_dir, f), 'w') as fout:
            score_order = [s for s in sorted(
                enumerate(c), key=lambda x: x[1], reverse=True
            )]
            summ_len = int(math.ceil(compression_rate*len(doc)))
            candidates = score_order[:summ_len]
            candidates_sorted = [cand for cand in sorted(
                candidates, key=lambda x: x[0]
            )]

            for cand_id, cand_score in candidates_sorted:
                candidate = doc[cand_id]
                for word in candidate:
                    fout.write(word)
                    fout.write(" ")
                fout.write("\n")
