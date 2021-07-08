#!/usr/bin/env python3
#html2ors.py

import os
import sys
import hashlib
from bs4 import BeautifulSoup

#Import the html file contents and open it with Beautiful Soup
arguments = len(sys.argv)
for a in range(1,arguments):
    html_file = open(sys.argv[a], "rb")
    file_name = html_file.name
    sys.stdout.write("Importing \"" + file_name + "\"...\n")
    soup = BeautifulSoup(html_file, "lxml")

    #Specific table elements extracted from the Beautiful Soup contents
    gs_results = soup.find_all('tr', class_= 'gsc_a_tr')

    #Obtain authorID from filename
    file_string = file_name.split("-")
    author_ID = file_string[0]

    #An array is created for each item in the Beautiful Soup file
    gs_lists = []
    for i in gs_results:
        item = i
        initial_link = i.a['data-href']
        prefaceURL = "https://scholar.google.com"
    
        #Create the necessary link information to cause a popup of the article
        adj_string = initial_link
        adj_string = adj_string.replace('/', '%2F')
        adj_string = adj_string.replace('?', '%3F')
        adj_string = adj_string.replace('=', '%3D')
        adj_string = adj_string.replace(':', '%3A')
        adj_string = adj_string.replace('&', '%26')
        popupURL = "/citations?user=" + author_ID + "#d=gs_md_cita-d&u=" + adj_string

        #Extract the specific elements of the HTML page contents
        directURL = prefaceURL + i.a['data-href']
        popURL = prefaceURL + popupURL
        title = i.a.text
        authors = i.select_one('.gs_gray').text
        source = i.select('.gs_gray')[-1].text
        citedBy = i.select_one('.gsc_a_ac')['href']
        citations = i.select_one('.gsc_a_ac').text
        pageYear = i.select_one('.gsc_a_y').text
        hash_string = title.lower()
        hash_ID = hashlib.md5(hash_string.encode())
        hashID = hash_ID.hexdigest()

        #Items are saved in array for ORS file
        gs_lists.append((
        hashID + ' ' + pageYear + ' { ' + \
        '"DirectURL":"' + directURL + '", ' + \
        '"PopURL":"' + popURL + '", ' + \
        '"Title":"' + title + '", ' + \
        '"Authors":"' + authors + '", ' + \
        '"Source":"' + source + '", ' + \
        '"CitedBy":"' + citedBy + '", ' + \
        '"Citations":"' + citations + '", ' + \
        '"PageYear":"' + pageYear + '"}'
        ))
         
        #Save the contents as an ORS file with the same name as the original HTML file
        f_name, f_ext = os.path.splitext(html_file.name)        
        with open((f_name + ".ors"), "w") as new_file:
            for line in gs_lists:
                new_file.write("".join(line) + "\n") 
    sys.stdout.write('Saving as "' + new_file.name + '" ...\n') 
    html_file.close()
 
    
