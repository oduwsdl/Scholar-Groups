#!/usr/bin/env python3
#dedup.py

import sys
import fileinput

"""
This program examines entries in an ORS file to remove duplicates. The 
program is designed to take a filename as input or to read lines from 
the Command Line Interface. Currently, it displays unique entries using 
the STDOUT function. However, it can easily be revised to display those 
entries that are duplicates. The program functions by examining the 
first key in the ORS file and storing it in an array. After that first 
entry is stored, the hash key value is extracted from each line and 
compared with the array. If no duplicate entry is found, the line is 
sent to the STDOUT function, and the hash key is added to the array. If 
the hash is already found in the array, the link is skipped.  
"""

# Import the ORS file contents and compare hash key values
ors_comp = []
first_word = []
duplicates = []
for line in fileinput.input():
    firstword = line.split(' ', 1)[0]
    if firstword in first_word:
        duplicates.append(firstword)
        # sys.stdout.write(line)  # Used as needed to list duplicates

    if firstword not in first_word:
        first_word.append(firstword)
        ors_comp.append(line)
        sys.stdout.write(line)
