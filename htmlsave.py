#!/usr/bin/env python3
#htmlsave.py

import os
import sys
import requests
from datetime import date 

def createfilename():
    filename = (authorID + "-" + str(today) + "-" + str("%04d" % begin_value) + \
                         "-" + str("%04d" % end_value) + ".html")
    return filename

#Import author IDs from command line and download Google Scholar webpages
arguments = len(sys.argv)
today = date.today()
for a in range(1,arguments):
    authorID = sys.argv[a]
    sys.stdout.write("Processing Author ID " + authorID + " . . .\n")

    #Loop through the program to download author ID webpages
    begin_value = 0
    end_value = 100 
    url = ("https://scholar.google.com/citations?hl=en&user=" + authorID + \
           "&view_op=list_works&sortby=pubdate&cstart=" + str(begin_value) + \
           "&pagesize=" + str(end_value))
    page = requests.get(url)
    
    #Program checks status code to verify a valid page was received
    statuscode = page.status_code
    if statuscode == 200:
        begin_value = begin_value + 1
        new_filename = createfilename()
        if os.path.exists(new_filename):
            sys.stdout.write("Overwriting existing file with same name ...\n")
        else:
            sys.stdout.write("Creating new file ...\n")
        html_file = open(new_filename, "wb")
        html_file.write(page.content)
        html_file.close()
        sys.stdout.write("File saved as \"" + html_file.name + "\"\n")
    if statuscode != 200:
        sys.stderr.write("Incorrect author ID or inaccessible webpage.\n")
        continue
    
