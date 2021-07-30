#!/usr/bin/env python3
#orsconvert.py

import sys
import argparse
import fileinput

"""
This program imports entries structured in a dictionary-type key/value format and converts
the entries to JSON, BIBTEX, or HTML. The program is run from the Command Line Interface and 
can read from STDIN or accept a designated file as input. The arguments --json, --bibtex, or 
--html identify the desired output, which can be displayed through STDOUT or saved as a file. 
The argparse library is imported to recognize and interpret the specified arguments. 

The createjson() function is designed to import the ORS entries and convert them into a JSON 
recognized format. Normal JSON conventions are used, such as brackets for an [array], and a 
space after the colon in the "Key": "Value" pairings. The function is separated from the main 
portion of code to facilitate any future need for revision. Currently, the function uses 
simply string replacement to extract and format the information. Originally, the attempt was 
made to parse the items with a dictionary library, but this created errors if quotation marks 
were part of a title, which was the case in at least one instance. For example, an article 
title of "Why are some files "lost" in the cloud?" would often be identified as two fields
instead of one. Because titles and source information listings often contain quotation marks 
and colons, it seemed that a dictionary parser was not a good choice. 

The createbibtex() function imports the ORS entries and converts them to BIBTEX format. In 
this case, all entries are specified as "@misc" types as there is no easy way to identify 
the actual type of entry from the often-abbreviated notation used by Google Scholar. There 
are two deviations from normal BIBTEX conventions: (1) Instead of only having one set of 
curly braces around all authors, each author is also in braces. This was done so that any 
BIBTEX interpreter would not convert initials to lowercase as if they were a full name. 
Thus, the field entry is "author = {{ML Nelson} and {MC Weigle} and {SM Jones}}" here. 
(2) A comma is provided at the end of every entry even though this is not required as it 
provided better identification if added fields are appended. 

The createhtml() function imports the ORS entries and converts them to an HTML style list. 
Because HTML files require lines of code before and after a list to identify document type, 
style, title, head, and body, the function is more involved than the other functions. The 
program does not currently use a specified style, but the line in the code remains, being 
commented out, so that a user can easily include that functionality. Additionally, the 
program allows the user to specify the title for the webpage if desired using the optional 
"--title" argument with a subsequent title. All list entries are inclosed within <ol> tags 
to identify them as an ordered list. 
"""

# This function converts the entries in an ORS file to the conventional JSON format. Each
# entry is identified with a hash of the title followed by the year of publication.
def createjson():
    for line in fileinput.input(args.inputfile):
        item_hash,item_year,item_list = line.split(' ', 2)
        item_list = item_list.replace('":"', '": "')
        directURL, title, authors, source, citedby, citations, pageyear = item_list.split('", "')
        directURL = directURL.replace('{ "', '"')
        directURL = (directURL + '"')
        title = ('"' + title + '"')
        authors = ('"' + authors + '"')
        if ',' in authors:
            authors = authors.replace(', ', '",\n        "')
            authors = authors.replace('": "', '": [\n        "') 
            authors = (authors + '\n    ]') 
        source = ('"' + source + '"')
        citedby = ('"' + citedby + '"')
        citations = citations.replace('": "', '": ')
        citations = ('"' + citations)
        pageyear = pageyear.replace('": "', '": ')
        pageyear = pageyear.replace('"}\n', '')
        pageyear = ('"' + pageyear)
        json_entry = (item_hash + ' ' + item_year + ' \n{ \n    ' + directURL + ',\n    ' + \
                      title + ',\n    ' + authors + ',\n    ' + source + ',\n    ' + \
                      citedby + ',\n    ' + citations + ',\n    ' + pageyear + \
                      '\n}\n')
        sys.stdout.write(json_entry +"\n")

# This function converts the entries in an ORS file to the conventional BIBTEX format. Each 
# entry is identified as "@misc" type in the current configuration. Additionally, when the 
# author field has multiple authors, each author is also enclosed in curly braces {}.
def createbibtex():
    for line in fileinput.input(args.inputfile):
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
        bibtex_entry = ('@misc{' + item_hash + ':' + item_year + ',\n      ' + \
                        title + '},\n      ' + authors + '},\n      ' + \
                        pageyear + '},\n      ' + source + '},\n      ' + \
                        directURL + '},\n},\n')  #  A non-conventional comma ends entries
        sys.stdout.write(bibtex_entry +"\n")

# This function converts the entries in an ORS file into HTML format. The entries are 
# formatted as an ordered list. The user may specify a page title if desired. 
def createhtml():
    sys.stdout.write('<html>\n')
    sys.stdout.write('<head>\n')
    sys.stdout.write('<title>' + args.title + '</title>\n')
    #    sys.stdout.write('<link rel="stylesheet" type="text/css" href="https://www.odu.edu:"></head>\n')
    sys.stdout.write('<body bgcolor="white">\n')
    sys.stdout.write('<h2>' + args.title + '</h2>\n')
    sys.stdout.write('<p> </p>\n')
    sys.stdout.write('<ol>\n')
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
        sys.stdout.write('<li>' + authors + ', <b><a href="' + directURL + '">' + title + '</a></b>, ' + \
                         source + '.<p> </p></li>\n')
    sys.stdout.write('</ol>\n')
    sys.stdout.write('</body>\n')
    sys.stdout.write('</html>\n') 

"""
The program is designed to be run from the Command Line Interface. The Argparse library
is imported to define and recognize arguments. Currently, --json, --bibtex, and --html 
are the three options for exported formats. Although convention indicates that "--" on 
the front of an argument makes it optional, these three formats are configured so that 
one argument is required, and only one may be selected. An optional "--title" argument 
is included so that the user may designate the title of the page; this is only useful 
when the --html option is selected. 
""" 

parser = argparse.ArgumentParser(description='Converts ORS file to selected filetype')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--json', action='store_true', help='Converts to JSON format')
group.add_argument('--bibtex', action='store_true', help='Converts to BIBTEX format')
group.add_argument('--html', action='store_true', help='Converts to HTML format')
parser.add_argument('--title', type=str, help='Provides title for HTML page if desired')
parser.add_argument('inputfile', type=str, nargs='?', help='enter the ORS file name')
args = parser.parse_args()

# The user can select the format argument option to be called.
if args.json:
    createjson()
           
elif args.bibtex:
    createbibtex()

elif args.html:
    createhtml()
 

    
