#!/usr/bin/env python3
#dedup.py

import sys
import fileinput

#Import the ORS file contents and compare hash key values
ors_comp = []
first_word = []
duplicates = []
    for line in fileinput.input():
        firstword = line.split(' ', 1)[0]
        if firstword in first_word:
            duplicates.append(firstword)
        if firstword not in first_word:
            first_word.append(firstword)
            ors_comp.append(line)
            sys.stdout.write(line)
