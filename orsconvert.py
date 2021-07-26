#!/usr/bin/env python3
import sys
import argparse
import fileinput

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

def createbibtex():
    for line in fileinput.input(args.inputfile):
        item_hash,item_year,item_list = line.split(' ', 2)
        directURL, title, authors, source, citedby, citations, pageyear = item_list.split('", "')
        directURL = directURL.replace('{ "DirectURL":"', 'url = {')
        title = title.replace('Title":"', 'title = {')
        authors = authors.replace('Authors":"', 'author = {')
        authors = authors.replace(',', ' and')
        source = source.replace('Source":"', 'howpublished = {')
        pageyear = pageyear.replace('PageYear":"', 'date = {') 
        pageyear = pageyear.replace('"}\n', '') 
        bibtex_entry = ('@misc{' + item_hash + ':' + item_year + ',\n      ' + \
                        title + '},\n      ' + authors + '},\n      ' + \
                        pageyear + '},\n      ' + source + '},\n      ' + \
                        directURL + '},\n},\n')
        sys.stdout.write(bibtex_entry +"\n")

def createhtml():
    sys.stdout.write('<html>\n')
    sys.stdout.write('<head>\n')
    sys.stdout.write('<title>Web Sciences and Digital Libraries Research Group</title>\n')
    sys.stdout.write('<link rel="stylesheet" type="text/css" href="https://www.odu.edu:"></head>\n')
    sys.stdout.write('<body bgcolor="white">\n')
    sys.stdout.write('<script type="text/javascript"> var gaJsHost = (("https:" == document.location.protocol) ? \
                     "https://ssl." : "http://www.");document.write(unescape("%3Cscript src=\'" + gaJsHost + \
                     "google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E"));</script>\n')
    sys.stdout.write('<script src="https://ssl.google-analytics.com/ga.js" type="text/javascript"></script>\n')
    sys.stdout.write('<script type="text/javascript"> var pageTracker = _get._getTracker("UA-5691952-1"); \
                     pageTracker._trackPageview();</script>\n')
    sys.stdout.write('<h2>Web Sciences and Digital Libraries Research Group</h2>\n')
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
                         source + ', ' + pageyear + '.<p> </p></li>\n')
    sys.stdout.write('</ol>\n')
    sys.stdout.write('</body>\n')
    sys.stdout.write('</html>\n') 

parser = argparse.ArgumentParser(description='Converts ORS file to selected filetype')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--json', action='store_true', help='Converts to JSON format')
group.add_argument('--bibtex', action='store_true', help='Converts to BIBTEX format')
group.add_argument('--html', action='store_true', help='Converts to HTML format')
parser.add_argument('inputfile', type=str, nargs='?', help='enter the ORS file name')
args = parser.parse_args()

if args.json:
    createjson()
           
elif args.bibtex:
    createbibtex()

elif args.html:
    createhtml()
 

    
