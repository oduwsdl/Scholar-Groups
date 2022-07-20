#!/usr/bin/env python3
#html2ukvs.py

import os
import sys
import urllib
import hashlib
from bs4 import BeautifulSoup
import argparse
import math

"""
The findinitiallink(): function is used to search the saved HTML file for the link for each 
article. Originally, this was simply included in the main code. However, Google Scholar has 
revised their code, which required this to be revised as well. This was now converted to a 
separate function so that it is easier to identify and revise as necessary. The function is 
currently set to capture the link according to either the previous GS coding or the current 
GS coding. It finds the link and returns it to the main program where it was called.
The createpopupURL() function is used to create the link necessary to cause the GS article 
link to open the article in a popup window. Originally, this was part of the main code. It 
currently does not work as Google Scholar has removed that functionality from the webpage. 
However, the function has been separated from the code and left intact in case the ability
is again available through the GS website.
"""


# This function is called from the main program code to find the link for each article using 
# Beautiful Soup analysis and return that link to the code where it was called. 
def findinitiallink(i):
    if 'data-href' in i:
        initial_link = i.a['data-href']
    else:
         initial_link = i.select_one('.gsc_a_t a')['href']
    return initial_link 

# This function is called from the main program to create a link that opens the article in a 
# popup window. It currently does not operate in Google Scholar, but is here for future use. 
def createpopupURL(initial_link):
    encoded_link = urllib.parse.quote(initial_link, safe='')
    popupURL = prefaceURL + '/citations?user=' + author_ID + '#d=gs_md_cita-d&u=' + encoded_link
    return popupURL 

"""
The main program code uses Beautiful Soup to extract article contents from the HTML file. 
Currently, the program runs from the Command Line Interface. The user must specify the 
name of the HTML file to convert to UKVS type. The program can convert one or multiple HTML 
files. Additionally, the program saves the file in the same naming convention as the name 
of the original HTML file.
"""

# If author ID starts with '-', add '\' in front of it to avoid argument parsing errors.
sys.argv = list(map(lambda st: st.replace('-', '\-', 1) if st != '-i' and st[0] == '-' else st, sys.argv))

parser = argparse.ArgumentParser()
# Add parser argument for the files that will be converted
parser.add_argument('files', action='append', nargs='+')
# Add parser argument for the scholar IDs and their start years and end years.
parser.add_argument('-i', action='append', nargs='+')
args = parser.parse_args()

files = args.files[0]
scholar_options = { option[0]: list(map(int, option[1:])) for option in args.i }
# Import the html file contents and open it with Beautiful Soup. The HTML file is read by 
# byte and uses the 'lxml' conversion parser. This uses Beautiful Soup version 4.
arguments = len(sys.argv)
if arguments == 1:
    sys.stdout.write('No HTML articles were identified for conversion ...\n')
for file in files:
    html_file = open(file, 'rb')
    file_name = html_file.name
    sys.stdout.write('Importing "' + file_name + '" ...\n')
    soup = BeautifulSoup(html_file, 'lxml')

    # Specific table elements extracted from the BS contents. Although most of the useful 
    # information is in the <td> fields, the entire <tr> field is captured to guarantee it.
    gs_results = soup.find_all('tr', class_= 'gsc_a_tr')

    # Obtain authorID from filename. No simple field is available in the HTML to extract the
    # ID using Beautiful Soup, so it is extracted from the file name using the string separator.
    file_string = file_name.split('XXXXXXX')
    author_ID = file_string[1]

    scholar_id_key = author_ID.replace('-', '\-', 1) if author_ID[0] == '-' else author_ID
    
    startyear, endyear = -math.inf, math.inf
    if scholar_id_key in scholar_options.keys():
        startyear, endyear = scholar_options[scholar_id_key]

    """
    The program uses Beautiful Soup functions to extract specific elements. The elements are 
    extracted from the HTML file on a line-by-line basis, which is then saved in an array format 
    to the UKVS file. This facilitates each entry still being a single line in the UKVS file that 
    contains all the required elements in a specified format. 
    """

    # An array is created for each item in the Beautiful Soup file. Contents are extracted 
    # from the BS file on a line-by-line basis.
    gs_lists = []
    for i in gs_results:
        item = i
        initial_link = findinitiallink(i)
        prefaceURL = 'https://scholar.google.com'

        append = False
    
        # Specific elements of the HTML page contents are extracted using Beautiful Soup 
        # field selection keys. These are more precise and concise than "find" and "findall"

        pageYear = i.select_one('.gsc_a_y').text

        if pageYear.isnumeric():
            if int(pageYear) >= startyear and int(pageYear) <= endyear:
                # If the extracted page year is within the bounds of the entered start year and end year,
                # set append to true
                append = True

        if append:    
            directURL = prefaceURL + initial_link
            #popURL = createpopupURL(initial_link)  #Used previously to create popup URL link
            title = i.a.text
            authors = i.select_one('.gs_gray').text
            source = i.select('.gs_gray')[-1].text
            citedBy = i.select_one('.gsc_a_ac')['href']
            citations = i.select_one('.gsc_a_ac').text
            hash_string = title.lower()
            hash_ID = hashlib.md5(hash_string.encode())
            hashID = hash_ID.hexdigest()

            # Items in the UKVS file are arrays of entries with each entry being saved as 
            # multiple key-value pairs in a dictionary format following a hash and year key..
            gs_lists.append((
            hashID + ' ' + pageYear + ' { ' + \
            '"DirectURL":"' + directURL + '", ' + \
            #'"PopURL":"' + popURL + '", ' + \  # Removed while no longer functional in GS page
            '"Title":"' + title + '", ' + \
            '"Authors":"' + authors + '", ' + \
            '"Source":"' + source + '", ' + \
            '"CitedBy":"' + citedBy + '", ' + \
            '"Citations":"' + citations + '", ' + \
            '"PageYear":"' + pageYear + '"}'
            ))
            
            # Save the contents as an UKVS file with the same name as the original HTML file
            f_name, f_ext = os.path.splitext(html_file.name)
            with open((f_name + '.ukvs'), 'w') as new_file:
                for line in gs_lists:
                    new_file.write(''.join(line) + '\n') 
    sys.stdout.write('Saving as "' + new_file.name + '" ...\n') 
    html_file.close()