#!/usr/bin/env python3
#ukvsconvert.py

import sys
import argparse
import fileinput
import json
import re


"""
This program imports entries structured in a dictionary-type key/value format and converts
the entries to JSON, BIBTEX, or HTML. The program is run from the Command Line Interface and 
can read from STDIN or accept a designated file as input. The arguments --json, --bibtex, or 
--html identify the desired output, which can be displayed through STDOUT or saved as a file. 
The argparse library is imported to recognize and interpret the specified arguments. 


The createjson() function is designed to import the UKVS entries and convert them into a JSON 
recognized format. Normal JSON conventions are used, such as brackets for an [array], and a 
space after the colon in the "Key": "Value" pairings. The function is separated from the main 
portion of code to facilitate any future need for revision. Currently, the function uses 
simply string replacement to extract and format the information. Originally, the attempt was 
made to parse the items with a dictionary library, but this created errors if quotation marks 
were part of a title, which was the case in at least one instance. For example, an article 
title of "Why are some files "lost" in the cloud?" would often be identified as two fields
instead of one. Because titles and source information listings often contain quotation marks 
and colons, it seemed that a dictionary parser was not a good choice. 


The createbibtex() function imports the UKVS entries and converts them to BIBTEX format. In 
this case, all entries are specified as "@misc" types as there is no easy way to identify 
the actual type of entry from the often-abbreviated notation used by Google Scholar. There 
are two deviations from normal BIBTEX conventions: (1) Instead of only having one set of 
curly braces around all authors, each author is also in braces. This was done so that any 
BIBTEX interpreter would not convert initials to lowercase as if they were a full name. 
Thus, the field entry is "author = {{ML Nelson} and {MC Weigle} and {SM Jones}}" here. 
(2) A comma is provided at the end of every entry even though this is not required as it 
provided better identification if added fields are appended. 


The createhtml() function imports the UKVS entries and converts them to an HTML style list. 
Because HTML files require lines of code before and after a list to identify document type, 
style, title, head, and body, the function is more involved than the other functions. The 
program does not currently use a specified style, but the line in the code remains, being 
commented out, so that a user can easily include that functionality. Additionally, the 
program allows the user to specify the title for the webpage if desired using the optional 
"--title" argument with a subsequent title. All list entries are inclosed within <ol> tags 
to identify them as an ordered list. 
"""


# This function converts the entries in an UKVS file to the conventional JSON format. Each
# entry is identified with a hash of the title followed by the year of publication.

def createjson():
    sys.stdout.write('{\n' +  '"Article Results": [')
    inp = fileinput.input(args.inputfile)
    for idx,line in enumerate(inp):
        if idx > 0:
            sys.stdout.write(',\n')
        item_hash,item_year,item_list = line.split(' ', 2)
        item_list = item_list.replace('":"', '": "')
        directURL, title, authors, source, citedby, citations, pageyear = item_list.split('", "')
        directURL = directURL.replace('{ "', '"')
        directURL = (directURL + '"')
        
        # Split the title
        title_list = title.split('Title":')
        # JSON encode the title
        actual_title = json.dumps(title_list[1][2:])
        title = 'Title": ' + actual_title
        title = ('"' + title)
        
        authors = ('"' + authors + '"')
        if ',' in authors:
            authors = authors.replace(', ', '",\n        "')
            authors = authors.replace('": "', '": [\n        "') 
            authors = (authors + '\n    ]') 
        source_list = source.split('Source":')
        actual_source = json.dumps(source_list[1][2:])
        source = 'Source": ' + actual_source
        source = ('"' + source)
        citedby = ('"' + citedby + '"')
        if citations == '": "':
           citations = citations.replace('": "', '": ')
           citations = ('"' + citations)
        else: 
             citations = ('"' + citations + '"')
        if pageyear == '": "':
           pageyear = pageyear.replace('": "', '": ')
           pageyear = pageyear.replace('"}', '')
           pageyear = ('"' + pageyear)
        else:
             pageyear = ('"' + pageyear)
        json_entry = (' \n{ \n    ' + directURL + ',\n    ' + 
                      title + ',\n    ' + authors + ',\n    ' + source + ',\n' +
                      citedby + ',\n    ' + citations + ',\n    ' + pageyear )
        sys.stdout.write(json_entry)
    sys.stdout.write(']' + '}')
# This function converts the entries in an UKVS file to the conventional BIBTEX format. Each 
# entry is identified as "@misc" type in the current configuration. Additionally, when the 
# author field has multiple authors, each author is also enclosed in curly braces {}.

def createbibtex():
    for line in fileinput.input(args.inputfile):
        #print(line)
        item_hash,item_year,item_list = line.split(' ', 2)
        directURL, title, authors, source, citedby, citations, pageyear = item_list.split('", "')
        directURL = directURL.replace('{ "DirectURL":"', 'url = {')
        title = title.replace('Title":"', 'title = {')
        authors = authors.replace('Authors":"', 'author = {')
        if ',' in authors: 
            authors = (authors + '}')
            authors = authors.replace('{', '{{')
            authors = authors.replace(', ', '} and {')
        source = source.replace('Source":"', 'howpublished = {')
        pageyear = pageyear.replace('PageYear":"', 'date = {') 
        pageyear = pageyear.replace('"}\n', '') 
        bibtex_entry = ('@misc{' + item_hash + ':' + item_year + ',\n      ' + 
                        title + '},\n      ' + authors + '},\n      ' + 
                        pageyear + '},\n      ' + source + '},\n      ' + 
                        directURL + '},\n},\n')  #  A non-conventional comma ends entries
        sys.stdout.write(bibtex_entry +"\n")

def createmd():
    sys.stdout.write('# ' + args.title +'\n')
    #sys.stdout.write('<p> </p>\n')


    entries = []
    start = float("inf")
    end = -float("inf")

    for line in fileinput.input(args.inputfile):
        item_hash,item_year,item_list = line.split(' ', 2)
        directURL, title, authors, source, citedby, citations, pageyear = item_list.split('", "')
        directURL = directURL.replace('{ "DirectURL":"', '')
        title = title.replace('Title":"', '')
        authors = authors.replace('Authors":"', '')
        source = source.replace('Source":"', '')
        citedby = citedby.replace('CitedBy":"', '')
        pageyear = pageyear.replace('PageYear":"', '') 
        pageyear = pageyear.replace('"}\n', '')
        if source == 'Source":"':
             source = pageyear.replace('PageYear":"','') 
        else:
              source = source.replace('Source":"', '')

        try:
            entries.append((authors, directURL, title, source, int(pageyear)))
            start = min(int(pageyear), start)
            end = max(int(pageyear), end)
        except: # YEAR NOT PROVIDED - WILL FIX
            entries.append((authors, directURL, title, source, 0))

    if args.startyear:
        start = int(args.startyear)
    if args.endyear:
        end = int(args.endyear)

    if args.list == 'all':
        prevyear = None
        for item in entries:
            year = int(item[4])
            if year < start or year > end:
                continue
            if year != prevyear: 
                sys.stdout.write('## ' + str(year) + '\n')
            sys.stdout.write('1. ' + item[0] + ', <b><a href="' + item[1] + '">' + item[2] + '</a></b>, ' + \
                             item[3] + '.<p> </p>\n')
            prevyear = year
    elif args.list == '1':
        prevyear = None
        for item in entries:
            year = int(item[4])
            if year < start or year > end:
                continue
            if year != prevyear:
                sys.stdout.write('   ## ' + str(year) + '\n')
            sys.stdout.write('1. ' + item[0] + ', <b><a href="' + item[1] + '">' + item[2] + '</a></b>, ' + \
                             item[3] + '.<p> </p>\n')
            prevyear = year
    elif args.list =='none' or args.list is None:
        for item in entries:
            year = int(item[4])
            if year < start or year > end:
                continue
            sys.stdout.write('1. ' + item[0] + ', <b><a href="' + item[1] + '">' + item[2] + '</a></b>, ' + \
                             item[3] + '.<p> </p>\n')



def createhtml():
    sys.stdout.write('<html>\n')
    sys.stdout.write('<head>\n')
    sys.stdout.write('<title>' + args.title + '</title>\n')
    sys.stdout.write('<body bgcolor="white">\n')
    sys.stdout.write('<h2>' + args.title + '</h2>\n')
    sys.stdout.write('<p> </p>\n')

    entries = []
    start = float("inf")
    end = -float("inf")

    for line in fileinput.input(args.inputfile):
        item_hash,item_year,item_list = line.split(' ', 2)
        directURL, title, authors, source, citedby, citations, pageyear = item_list.split('", "')
        directURL = directURL.replace('{ "DirectURL":"', '')
        title = title.replace('Title":"', '')
        authors = authors.replace('Authors":"', '')
        citedby = citedby.replace('CitedBy":"', '')
        pageyear = pageyear.replace('PageYear":"', '') 
        pageyear = pageyear.replace('"}\n', '')
        if source == 'Source":"':
             source = pageyear.replace('PageYear":"','') 
        else:
              source = source.replace('Source":"', '')

        try:
            entries.append((authors, directURL, title, source, int(pageyear)))
            start = min(int(pageyear), start)
            end = max(int(pageyear), end)
        except: # YEAR NOT PROVIDED - WILL FIX
            entries.append((authors, directURL, title, source, 0))

    if args.startyear:
        start = int(args.startyear)
    if args.endyear:
        end = int(args.endyear)

    if args.list == 'all':
        prevyear = None
        for item in entries:
            year = int(item[4])
            if year < start or year > end:
                continue
            if year != prevyear:
                if prevyear is not None:
                    sys.stdout.write("</ol>")
                sys.stdout.write('<h2>' + str(year) + '</h2>\n<ol>\n')
            sys.stdout.write('<li>' + item[0] + ', <b><a href="' + item[1] + '">' + item[2] + '</a></b>, ' + \
                             item[3] + '.<p> </p></li>\n')
            prevyear = year
    elif args.list == '1':
        prevyear = None
        sys.stdout.write("<ol>\n")
        for item in entries:
            year = int(item[4])
            if year < start or year > end:
                continue
            if year != prevyear:
                sys.stdout.write('<h2>' + str(year) + '</h2>\n')
            sys.stdout.write('<li>' + item[0] + ', <b><a href="' + item[1] + '">' + item[2] + '</a></b>, ' + \
                             item[3] + '.<p> </p></li>\n')
            prevyear = year
        sys.stdout.write("</ol>")
    elif args.list =='none' or args.list is None:
        for item in entries:
            year = int(item[4])
            if year < start or year > end:
                continue
            sys.stdout.write('<li>' + item[0] + ', <b><a href="' + item[1] + '">' + item[2] + '</a></b>, ' + \
                             item[3] + '.<p> </p></li>\n')
    sys.stdout.write('</body>\n')
    sys.stdout.write('</html>\n')


"""

The program is designed to be run from the Command Line Interface. The Argparse library
is imported to define and recognize arguments. Currently, --json, --bibtex, --md, and --html 
are the four standard options for exported formats. You may also change HTML ordered list
views using the --html2 argument. Although convention indicates that "--" on the front of 
an argument makes it optional, these three formats are configured so that one argument is 
required, and only one may be selected. An optional "--title" argument is included so that 
the user may designate the title of the page; this is only useful when the --html option is 
selected. An optional "--sort" argument is available to allow the user to sort articles by 
a specify a range of years, "start_year - end_year".

""" 

parser = argparse.ArgumentParser(description='Converts UKVS file to selected filetype')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--json', action='store_true', help='Converts to JSON format')
group.add_argument('--bibtex', action='store_true', help='Converts to BIBTEX format')
group.add_argument('--md', action='store_true', help='Converts to Markdown format')
group.add_argument('--html', action='store_true', help='Converts to HTML format')
parser.add_argument('--title', type=str, help='Provides title for HTML page if desired')
parser.add_argument('--startyear', type=str, help='Sort by specified start year')
parser.add_argument('--endyear', type=str, help='Sort by specified end year')
parser.add_argument('--list', type=str, help='Specify Ordered List Format')
parser.add_argument('inputfile', type=str, nargs='?', help='enter the UKVS file name')
args = parser.parse_args()


# The user can select the format argument option to be called.
if args.json:
    createjson()    

elif args.bibtex:
      createbibtex()

elif args.md:
      createmd()

elif args.html:
      createhtml()