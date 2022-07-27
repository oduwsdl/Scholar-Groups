#!/usr/bin/env python3
#htmlsave.py

import os
import sys
import argparse
import requests
from datetime import date 

"""
The "createfilename()" function uses a specific ID separator of 'XXXXXXX' before and 
after the author ID value. Originally, the file would start with the author ID and 
have the date string appended to it. However, some author IDs in Google Scholar will 
contain hyphens '-' and underscores '_' that create significant errors when trying 
to process commands from the Command Line Interface. For example, one author in the 
WSDL group has an ID in the form "-eRx..." that is read as an optional argument in 
Linux. Prefacing it with \ can work with manually-entered commands, but this is not 
as easily implemented when using automated scripts. Therefore, a regular character 
separator was added. Currently, 7 sets of 'X' is used as that is unlikely to be seen 
in an actual author ID field. The date field is added to identify when the content 
has been downloaded from Google Scholar. This provides a record to reflect changes 
to the website and content over time. The beginning and ending strings are used to 
capture a range of articles due to pagination issues where GS only displays some of 
the articles at any time. Originally, GS showed only a certain range of pages, then 
the code was revised to display all articles, then it reverted back to showing only
a range of articles/page. These are now set to 4 digits to capture from 0001 - 9999 
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
    end_value = (begin_value + 99) 
    filename = (id_separator + authorID + id_separator + '-' + str(today) + '-' + \
                str('%04d' % begin_value) + '-' + str('%04d' % end_value) + '.html')
    return filename

# This function formats the URL that is used to capture the HTML content. 
# The URL captures articles sorted according to most recent publication date.
def createURL():
    captureURL = ('https://scholar.google.com/citations?hl=en&user=' + authorID + \
                  '&view_op=list_works&sortby=pubdate&cstart=' + str(begin_value) + \
                  '&pagesize=' + str(page_size))
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
if arguments == 3:
    sys.stdout.write('No author IDs provided to process ...\n')
for a in range(3,arguments):
    authorID = sys.argv[a]
    sys.stdout.write('Processing Author ID ' + authorID + ' ...\n')

    # Loop through the program to download author ID webpages. Currently, the
    # Google Scholar website allows capturing of up to 100 articles at a time.
    start_value = 0
    begin_value = start_value
    page_size = 100 
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
    the author's updated ID. Additionally, the program uses a while loop to capture 
    additional pages of articles until it finds a specific qualifier string. The
    string ">There are no articles in this profile.<" is currently the qualifier. 
    """
    # Program requests further pages of articles until the qualifier string is found
    qualifier = '>There are no articles in this profile.<'
    article_test = True

    corrupted_file = '<p class="a2CQh" jsname="VdSJob">to continue to Google Scholar Citations</p>'

    # Program checks status code to verify a valid page was received. A status code 
    # of '200' is valid. A '302' redirect to a '200' is normally accepted as well.
    statuscode = page.status_code
    x = 1

    # Program loops to capture articles as long as qualifier is not found and the 
    # status code of '200' is registered.
    while statuscode == 200 and article_test == True:
        parser = argparse.ArgumentParser(description='Specify Output Location')
        parser.add_argument('--output', type=str, nargs ='?', required = True, help='Output Location')
        args, unknownargs = parser.parse_known_args()
        save_path = args.output
        new_filename = createfilename()
        if os.path.exists(new_filename):
            sys.stdout.write('Overwriting existing file with same name ...\n')
        else:
            sys.stdout.write('Creating new file ...\n')
        complete_Name = os.path.join(save_path, new_filename)
        html_file = open(complete_Name, 'wb')
        html_file.write(page.content)
        html_file.close()
        sys.stdout.write('File saved as "' + html_file.name + '"\n')
        begin_value = begin_value + 100
        page = requests.get(createURL())
        new_test = page.text
        if qualifier in new_test or corrupted_file in new_test:
            article_test = False 
        statuscode = page.status_code
        x = x+1

    # Program notifies user when no further articles are found within valid GS page
    if statuscode == 200 and article_test == False:
        sys.stdout.write('There are no more articles to capture ...\n')

    # Program notifies user when an invalid page is returned
    if statuscode != 200:
        sys.stderr.write('Incorrect author ID or inaccessible webpage.\n')
        continue

