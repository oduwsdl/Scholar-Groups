#!/usr/bin/env python3
#htmlsave.py

import os
import sys
import requests
from datetime import date 

"""
The "createfilename()" function uses a specific ID separator of 'XXXXXXX' before and 
after the author ID value. Originally, the file would start with the author ID and 
have the date string appended to it. However, some author IDs in Google Scholar will 
contain hyphens '-' and underscores '_' that create significant errors when trying 
to process commands from the Command Line Interface. Therefore, a regular character 
separator was added. Currently, 7 sets of 'X' is used as that is unlikely to be seen 
in an actual author ID field. The date field is added to identify when the content 
has been downloaded from Google Scholar. This provides a record to reflect changes 
to the website and content over time. The beginning and ending strings are used to 
capture a range of articles due to pagination issues where GS only displays some of 
the articles at any time. Originally, GS showed only a certain range of pages, then 
the code was revised to display all articles, then it reverted back to showing only
a range of articles/page. These are now set to 4 digits to capture from 0001 - 1000 
articles. The decision to use 4 digits instead of 3 digits was to prepare for the 
possibility that any user had more than 999 articles listed. 

The createURL() function provides the format of the URL to be captured by the program.  
Originally, this was within the main code. However, ongoing changes in the HTML code
for the Google Scholar webpage made it necessary to revise the code. Having this as 
a separate function facilitates future changes to the URL to be captured..
"""

# This function provides the format of the filename for saving the HTML content
# The file has the structure XXXXXXXauthorIDvalueXXXXXXX2021-08-14-0001-1000.html
def createfilename():
    id_separator = 'XXXXXXX'
    filename = (id_separator + authorID + id_separator + str(today) + '-' + str('%04d' % begin_value) + \
                         '-' + str('%04d' % end_value) + '.html')
    return filename

# This function formats the URL that is used to capture the HTML content. 
# The URL captures articles sorted according to most recent publication date.
def createURL():
    captureURL = ('https://scholar.google.com/citations?hl=en&user=' + authorID + \
                 '&view_op=list_works&sortby=pubdate&cstart=' + str(begin_value) + \
                 '&pagesize=' + str(end_value))
    return captureURL

"""
Originally, the program inquired of the user for an author ID, processed the ID to 
capture a webpage, and repeated the loop until the user indicated no further IDs to 
be processed. This was revised to run from the command line with author ID arguments 
without inquiry to the user. The 'sys.argv' library function is used to capture the 
author IDs from the command line. A loop is available to capture 100 articles at a 
time as that is the maximum that can be currently displayed in a single GS webpage 
within a single URL link. Capturing more would require additional automation.
"""

# Import author IDs from command line and download Google Scholar webpages
# The program loops through arguments to capture one or multiple author IDs. 
arguments = len(sys.argv)
today = date.today()
for a in range(1,arguments):
    authorID = sys.argv[a]
    sys.stdout.write('Processing Author ID ' + authorID + ' . . .\n')

    # Loop through the program to download author ID webpages. Currently, the
    # Google Scholar website allows capturing of up to 100 articles at a time.
    begin_value = 0
    end_value = 100 
    page = requests.get(createURL())
    
    """
    The status code of the requests.get function enables the program to verify 
    if a valid webpage has been received. If an invalid author ID is entered, a 
    status code '404' is received, and the HTML page is not downloaded. A simple 
   '302' redirect is allowed when the final page has the correct '200' status code.
    The one limitation is that the user must know the current author ID in order 
    to download articles. In cases where an author's ID has been changed, the 
    page will redirect in a way that gives a '302' redirect for users who are 
    logged into the Google Scholar service but gives a '404' for unknown users. 
    This program will not be recognized as a known user, so it cannot capture 
    the redirected page even when entering the URL in a browser would redirect 
    successfully. However, successfully navigating a redirect for changed author 
    IDs would not be useful because the new page shows only the first 20 articles 
    irrespective of the range provided in the original URL link. Therefore, it is 
    beneficial for the user to receive an error and be responsible for identifying 
    the author's updated ID. 
    """
    
    # Program checks status code to verify a valid page was received. A status code 
    # of '200' is valid. A '302' redirect to a '200' is normally accepted as well.
    statuscode = page.status_code
    if statuscode == 200:
        begin_value = begin_value + 1
        new_filename = createfilename()
        if os.path.exists(new_filename):
            sys.stdout.write('Overwriting existing file with same name ...\n')
        else:
            sys.stdout.write('Creating new file ...\n')
        html_file = open(new_filename, 'wb')
        html_file.write(page.content)
        html_file.close()
        sys.stdout.write('File saved as '" + html_file.name + '"\n')
    if statuscode != 200:
        sys.stderr.write('Incorrect author ID or inaccessible webpage.\n')
        continue
    
