#!/usr/bin/env python3
#dedup.py

import sys

#Import the ORS file contents and compare hash key values
ors_comp = []
first_word = []
duplicates = []
arguments = len(sys.argv)
for a in range(1,arguments):
    with open(sys.argv[a], "r") as ors_file:
        file_name = ors_file.name

        #An array is created for each item in the Beautiful Soup file
        ors_list = ors_file.readlines()
        for i in range(len(ors_list)):
            item = i
            firstword = ors_list[i].split(' ', 1)[0]
            if firstword in first_word:
                duplicates.append(firstword)
            if firstword not in first_word:
                first_word.append(firstword)
                ors_comp.append(ors_list[i])
                sys.stdout.write(ors_list[i])
