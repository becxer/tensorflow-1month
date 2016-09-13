#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import sys,re
import Hangul as hg

if len(sys.argv) < 3:
    print "./TextCleaner.py input-file output-file"
    sys.exit()

print_frq = 10000
input_file_name =  sys.argv[1]
output_file_name = sys.argv[2]
iof = open(input_file_name)

def replace_number(xs):
    return re.sub('[0-9]+',' NUMBER ', xs)

def replace_url(xs):
    return re.sub(r"http\S+", " URL ", xs)

oof = open(output_file_name,"w")
oof.write("")
oof.close()

count = 0
with open(input_file_name, 'rb') as fo:
    for line in fo : count += 1

for idx, line in enumerate(iof):
    if idx % print_frq == 0: 
        print "[%d/%d] processed.." % (idx, count)
    line = line.decode('utf-8')
    line = replace_url(line)
    line = replace_number(line)
    line = hg.remove_except_words(line).encode('utf-8').strip()
    if len(line) > 0:
        oof = open(output_file_name,"a")
        oof.write(line+"\n")
        oof.close()

print "Done"
