#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert texts in files of input_dir into corresponding numbers in dictionary
which is automatically generated according to the input datas.

Each output file has the same name as its input.
The generated dictionary is in the output_dir with name 'dictionary'
"""

__author__ = 'Lang-Chi Yu (yl871804@gmail.com)'
__license__ = 'Apache 2.0'
__version__ = '1.0.0'


from os import listdir, mkdir, path
from shutil import rmtree
from sys import argv


if len(argv) != 4:
    print "Usage: python token2enum.py <input_dir> <output_dir> <stop_words>"
    exit(1)

input_dir = argv[1]
output_dir = argv[2]
stop_words = argv[3]
if path.exists(output_dir):
    rmtree(output_dir)
mkdir(output_dir)

stop_words_list = []
with open(stop_words, 'r') as sw:
    for line in sw:
        stop_words_list.append(line.rstrip())

token2enum = {'': 0}
enum2token = ['']
stop_words_ids = []
for f in listdir(input_dir):
    with open(path.join(input_dir, f), 'r') as fin, \
        open(path.join(output_dir, f), 'w') as fout:
        for line in fin:
            tokens = line.rstrip().split()
            for token in tokens:
                token = token.lower()
                if token not in token2enum:
                    idx = len(enum2token)
                    if token in stop_words_list:
                        stop_words_ids.append(idx)

                    token2enum[token] = idx
                    enum2token.append(token)

                fout.write(str(token2enum[token]))
                fout.write(' ')
            fout.write('\n')

with open(path.join(output_dir, 'dictionary'), 'w') as dict_fout:
    for token in enum2token[1:]:
        dict_fout.write(token)
        dict_fout.write('\n')

with open(path.join(output_dir, 'stop_words'), 'w') as sw_out:
    for stop_word_id in stop_words_ids:
        sw_out.write(str(stop_word_id)+' ')

print "Dictionary size: " + str(len(enum2token)-1)
