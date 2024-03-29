## htmlsave.py
* [usage](README.md#htmlsavepy-usage)
* [createfilename](README.md#createfilename)
* [createURL](README.md#createURL)
* [examples](README.md#htmlsavepy-examples)
* [caveats](README.md#htmlsavepy-caveats)

The htmlsave.py program simply allows the user to enter specific author IDs for a Google Scholar page and, using those IDs, downloads the HTML pages associated with the author. The 'sys.argv' library function is used to capture the author IDs from the command line, and a loop allows the program to capture 100 articles at a time until all articles have been downloaded. This does 100 articles at a time and saves each webpage individually as its own file. 

### htmlsave.py usage
```
$ htmlsave.py [authorID]
```
The program will process one or more author IDs and save a page with up to 100 articles for each author. When an author has more than 100 articles, the remaining articles are saved in new files. The program uses the requests.get function to obtain the HTML content. The status code is used to verify if a valid webpage has been received. If an invalid author ID is entered, a status code '404' is received, and the HTML page is not downloaded. A simple '302' redirect is allowed when the final page has the correct '200' status code. The one limitation is that the user must know the current author ID in order to download articles. In cases where an author's ID has been changed, the page will redirect in a way that gives a '302' redirect for users who are logged into the Google Scholar service but gives a '404' for unknown users. Because this program will not be recognized as a known user, it cannot capture the redirected page even when entering the URL in a browser would redirect successfully. However, successfully navigating a redirect for changed author IDs would not be useful because the new page shows only the first 20 articles irrespective of the range provided in the original URL link. Therefore, it is beneficial for the user to receive an error and be responsible for identifying the author's updated ID. Additionally, the program uses a while loop to capture additional pages of articles until it finds a specific qualifier string. The string ">There are no articles in this profile.<" is currently the qualifier to identify when all articles have been captured.

To assist the user, the htmlsave.py program will advise the user when a new HTML file is overwriting another file by the same name, when an author ID is invalid, and when no further articles are available for download. 

The htmlsave.py program uses two functions for accessing Google Scholar: [createfilename](README.md#createfilename) and [createURL](README.md#createURL). 

### createfilename

The createfilename() function defines the format of the filename for the saved HTML pages. Originally, it was decided that the file would start with the author ID and have the date string and range of articles appended to it: 

* oWQaPnwAAAAJ-2021-08-01-001-100.html

However, some author IDs in Google Scholar will contain hyphens " - " and underscores " _ " that create significant errors when trying to process commands from the Command Line Interface. For example, one author in the WSDL group had an ID in the form "-eRsYx8AAAAJ" that was read as an optional argument in Linux. Prefacing it with \ would work with manually-entered commands, but this is not as easily implemented when using automated scripts. Therefore, a character separator string was added. Currently, a set of 7 'X's are used as that is unlikely to be seen in an actual author ID field; the separator is immediately before and after the authorID. The date field is then added to identify when the content has been downloaded from Google Scholar. This provides a record to reflect changes to the website and content over time. The beginning and ending strings are used to capture a range of articles due to pagination issues where GS only displays some of the articles at any time. Originally, GS showed only a certain range of pages, then the code was revised to display all articles, then it reverted back to showing only a range of articles/page. The range identifier in the filename is now set to 4 digits to the possibility to capture from 0001 - 9999 articles. The decision to use 4 digits instead of 3 digits was to prepare for the possibility that any user had more than 999 articles listed. The result is that filenames are saved as follows:

* XXXXXXX-eRxYs8AAAAJXXXXXXX-2021-08-01-0000-0099.html

### createURL

The createURL() function provides the format of the URL to be captured by the program.  Originally, this was within the main code. However, ongoing changes in the HTML code for the Google Scholar webpage made it necessary to revise the code. Having this as a separate function facilitates future changes to the URL to be captured. Currently, specific web fields precede and follow the authorID before the article range fields. 

* web_preface_html_code + authorID + article_selection_html_code + begin range + page_size_html_code + page size

And example initial webpage URL is as follows: 

https://scholar.google.com/citations?hl=en&user=oWQaPnwAAAAJ&view_op=list_works&sortby=pubdate&cstart=0&pagesize=100

The page size is set to capture 100 articles per page as that is the maximum presently allowable. 

### htmlsave.py examples

The program processes multiple author IDs as follows: 

```
$ ./htmlsave.py oWQaPnwAAAAJ OkEoChMAAAAJ -eRsYx8AAAAJ Lfu3j30AAAAJ QjHw7ugAAAAJ
Processing Author ID oWQaPnwAAAAJ ...
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0000-0099.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0100-0199.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0200-0299.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0300-0399.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0400-0499.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0500-0599.html"
There are no more articles to capture ...
Processing Author ID OkEoChMAAAAJ ...
Creating new file ...
File saved as "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-08-04-0000-0099.html"
There are no more articles to capture ...
Processing Author ID -eRsYx8AAAAJ ...
Creating new file ...
File saved as "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-08-04-0000-0099.html"
There are no more articles to capture ...
Processing Author ID Lfu3j30AAAAJ ...
Incorrect author ID or inaccessible webpage.
Processing Author ID QjHw7ugAAAAJ ...
Overwriting existing file with same name ...
File saved as "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.html"
There are no more articles to capture ...
$                                     
```

### htmlsave.py caveats

The htmlsave.py program is extremely basic, so it does not allow optional arguments. Every argument after the executable is considered an author ID value to be captured from the Google Scholar site. If '-h' is entered, the program will interpret that argument as an author ID and attempt to download a page associated with that value. This is a regrettable consequence of Google Scholar actually having some author IDs actually begin with the ' - ' character. 


## html2ors.py
* [findinitiallink](README.md#findinitiallink)
* [createpopupURL](README.md#createpopupURL)
* [examples](README.md#html2orspy-examples)
* [ORS file structure](README.md#ORS-file-structure)
* [caveats](README.md#html2orspy-caveats)

The html2ors.py program uses Beautiful Soup to extract article contents from the previously downloaded HTML files. Elements are extracted on a line-by-line basis. Currently, the program runs from the Command Line Interface. The user must specify the name of the HTML file to convert to ORS type. The program is designed to convert multiple HTML files. Additionally, the program saves the ORS file in the same naming convention as the name of the original HTML file, so it is relatively easy to identify which HTML files have been converted. 

* XXXXXXX-eRxYs8AAAAJXXXXXXX-2021-08-01-0000-0099.html &#8594;&#8594; XXXXXXX-eRxYs8AAAAJXXXXXXX-2021-08-01-0000-0099.ors

The program uses two specific functions as part of its operation: [findinitiallink](README.md#findinitiallink) and [createpopupURL](README.md#createpopupURL). 

### findinitiallink

The findinitiallink() function is used to search the saved HTML file for the URL for each article. Originally, this was simply included in the main code. However, Google Scholar had revised their code 3 weeks after the project began, which required this to be revised as well. This is now converted to a separate function so that it is easier to identify and revise as necessary. The function is currently set to capture the link according to either the previous GS coding or the current GS coding. It finds the link and returns it to the main program where it was called. 

An example of the current HTML code containing a link is as follows: 

```
<tr class="gsc_a_tr"><td class="gsc_a_t"><a href="/citations?view_op=view_citation&amp;hl=en&amp;oe=ASCII&amp;user=-eRsYx8AAAAJ&amp;pagesize=100&amp;sortby=pubdate&amp;citation_for_view=-eRsYx8AAAAJ:qsWQJNntlusC" class="gsc_a_at">...</a>
```
Here, the **"/citations?view_op=view_citation&amp;hl=en&amp;oe=ASCII&amp;user=-eRsYx8AAAAJ&amp;pagesize=100&amp;sortby=pubdate&amp;citation_for_view=-eRsYx8AAAAJ:qsWQJNntlusC"** portion must be extracted before it can be appended to an initial HTTP phrase to be used in the remainder of the program.  

### createpopupURL

The createpopupURL() function is used to create the link necessary to cause the GS article link to open the article in a popup window instead of just in a separate window. Originally, this was part of the main code but has been converted to a called function. It currently does not work as Google Scholar has removed that functionality from the webpage. However, the function has been left intact in case the ability again becomes available through the GS website.

### html2ors.py examples

The html2ors.py program converts multiple HTML files. Here, an example is provided showing how it processes multiple HTML files. Here, all HTML files are converted:

```
$ ./html2ors.py *.html
Importing "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-08-04-0000-0099.html" ...
Saving as "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-08-04-0000-0099.ors" ...
Importing "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-08-04-0000-0099.html" ...
Saving as "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-08-04-0000-0099.ors" ...
Importing "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.html" ...
Saving as "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0000-0099.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0000-0099.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0100-0199.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0100-0199.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0200-0299.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0200-0299.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0300-0399.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0300-0399.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0400-0499.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0400-0499.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0500-0599.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0500-0599.ors" ...
$     
```

### ORS file structure

The ORS file extracts specific fields for each article entry and formats them in a dictionary-type structure. Currently, there are nine (9) fields for each entry:
* Hash of title
* Year of publication
* DirectURL - URL to Google Scholar article
* Title - Title of article
* Authors - Authors associated with the article
* Source - Main source of article according to GS
* CitedBy - List of authors who have cited the article
* Citations - Number of times the article has been cited in GS
* PageYear - Year of publication

The ORS entry uses an MD5 hash of the title to assign a unique identifier to each article. Although the possibility of collision exists, it is relatively remote for the number of authors intended for this program. If the program is being used with a significantly larger number of authors, a different hash may be required. The year is also included twice in the ORS file. The year listing following the hash has been included to allow key sorting from the Command Line Interface. The seven (7) fields for the article itself are enclosed in {brackets} to indicate article information. 

```
2990027422b3de81a5abf997c5c94c18 2018 { "DirectURL":"https://scholar.google.com/citations?view_op=view_citation&hl=en&oe=ASCII&user=QjHw7ugAAAAJ&pagesize=100&sortby=pubdate&citation_for_view=QjHw7ugAAAAJ:2osOgNQ5qMEC", "Title":"How perceptions of web resource boundaries differ for institutional and personal archives", "Authors":"F Poursardar, F Shipman", "Source":"2018 IEEE international conference on information reuse and integration (iri …, 2018", "CitedBy":"https://scholar.google.com/scholar?oi=bibs&hl=en&oe=ASCII&cites=10120194878620841447", "Citations":"4", "PageYear":"2018"}        
```

### html2ors.py caveats

The html2ors.py program is extremely basic, importing one or more HTML files for conversion. Although it runs from the Command Line Interface, it does not recognize any optional arguments. All arguments following the executable are interpreted as HTML files to be imported and converted. If no file is listed after the executable, the program will display "No HTML files were identified for conversion ..." to the output. Additionally, it should be noted that some fields in the ORS entries may contain no information, such as when an article has not been cited, or may contain missing information, such as when ellipses " ... " replace author or source information. Because the program is capturing information from a Google Scholar page, it cannot provide information not listed there. 


## dedup.py
* [examples](README.md#deduppy-examples)
* [caveats](README.md#deduppy-caveats)

This program examines entries in an ORS file to remove duplicates. The program is designed to take a filename as input or to read lines from the Command Line Interface. Currently, it displays unique entries using the STDOUT function. However, it can easily be revised to display those entries that are duplicates. The program functions by examining the first key in the ORS file, which is the MD5 hash of the title, and storing it in an array. After the initial entry is stored, the hash key value is extracted from each line and compared with the array. If no duplicate entry is found, the line is sent to the STDOUT function, and the hash key is added to the array. If the hash is already found in the array, the program goes to the next line instead of sending the line to STDOUT. 

The dedup.py program is designed to filter out duplicate entries in a large list of articles. This is especially useful when compiling a database of articles by specific authors in which some articles are co-authored by members of the group. As such, the program works best when operating on multiple ORS files; however, it can evaluate entries in a single ORS file. 

### dedup.py examples

The dedup.py program operates as follows to remove duplicates from multiple ORS files, it is expected that the output will be redirected to a file instead of displayed on the screen. 

```
$ ./dedup.py *.ors > comprehensive.ors
$
$ wc *.ors
83   2804  44096 XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-08-04-0000-0099.ors
58   1890  32305 XXXXXXXOkEoChMAAAAJXXXXXXX-2021-08-04-0000-0099.ors
5    166   2846 XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.ors
100   2865  51103 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0000-0099.ors
100   2791  52788 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0100-0199.ors
100   2670  53349 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0200-0299.ors
100   2752  53807 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0300-0399.ors
100   2313  49950 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0400-0499.ors
45   1083  21616 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-08-04-0500-0599.ors
661  18568 346337 comprehensive.ors
1352  37902 708197 total
$           
```

In the above example, all the ORS files were processed by the dedup.py program, and unique entries were stored in the "comprehensive.ors" file. The "wc" function shows that there are a total of 691 entries before duplicates were removed (i.e., all ORS files excluding the comprehensive.ors file), and 661 unique entries were stored in the comprehensive.ors file. This indicates that 30 articles were identified as duplicates.


The data in an ORS file can be sorted by "year of publication" and displayed in descending order by using a combination of the sort by key "-k", reverse results of comparison "-r", and "-n" compare according to string numerical value bash arguments as shown below.

```
$ ./dedup.py *ors | sort -k2 -rn > comprehensive.ors
$ 
```

### dedup.py caveats

The dedup.py program is very basic, examining the hash values to identify duplicates. As such, it does not recognize optional arguments, and if no input it provided, it will simply wait. It uses the fileinput.input function to allow processing from a file or from STDIN, and it sends the results to STDOUT. It can process a single ORS file or multiple ORS files. Additionally, it should be noted that the program operates on the hash of the title as provided by Google Scholar. Therefore, the program is limited in its scope as it cannot differentiate beyond the hash of the title string. When different articles have the same title--such as conference presentations or papers with different years--or when the same article differs by a single character--such as a colon or comma--the program results may not be accurate. 


## orsconvert.py
* [createjson](README.md#createjson)
* [createbibtex](README.md#createbibtex)
* [createhtml](README.md#createhtml)
* [examples](README.md#orsconvertpy-examples)
* [caveats](README.md#orsconvertpy-caveats)

This program imports entries structured in a dictionary-type key/value format and converts the entries to JSON, BibTeX, or HTML. The program is run from the Command Line Interface. It can read from STDIN or accept a designated file as input, and it can read to STDOUT or be redirected to a file. The Argparse library is imported to define and recognize arguments. Currently, --json, --bibtex, and --html are the three standard options for exported formats. You may also change HTML ordered list views using the --html2 argument. Although convention indicates that "--" on the front of an argument makes it optional, these three formats are configured so that one argument is required, and only one may be selected. An optional "--title" argument is included so that the user may designate the title of the page; this is only useful when the --html option is selected. An optional "--sort" argument is available to allow the user to sort articles by a specify a range of years, "start_year - end_year". The results are displayed to the STDOUT output or can be pipelined to a file specified by the user. 

```
$ ./orsconvert.py -h
usage: orsconvert.py [-h] (--json | --bibtex | --html) [--title TITLE] [--sort SORT] [inputfile]

Converts ORS file to selected filetype

positional arguments:
  inputfile      enter the ORS file name
  
optional arguments:
  -h, --help     show this help message and exit
  --json         Converts to JSON format
  --bibtex       Converts to BibTeX format
  --html         Converts to HTML format
  --title TITLE  Provides title for HTML page if desired
  --sort SORT    Sort by specified range of years
$    
```

### createjson

The createjson() function is designed to import the ORS entries and convert them into a JSON recognized format. Normal JSON conventions are used, such as brackets [] for an array, and a space after the colon in the "Key": "Value" pairings. The function is separated from the main portion of code to facilitate any future need for revision. Currently, the function uses simple string replacement to extract and format the information. Originally, the attempt was made to parse the items with a dictionary library, but this created errors if quotation marks were part of a title, which was the case in at least one instance. For example, an article title of "Why are some files "lost" in the cloud?" would be identified as two fields instead of one. Because titles and source information listings often contain quotation marks and colons, it seemed that a dictionary parser was not a good choice. The output includes line breaks and indents to facilitate a user scanning the results. 

### createbibtex

The createbibtex() function imports the ORS entries and converts them to BibTeX format. In this case, all entries are specified as "@misc" types as there is no easy way to identify the actual type of entry from the often-abbreviated notation used by Google Scholar. There are two deviations from normal BibTeX conventions: (1) Instead of only having one set of curly braces around all authors, each author is also in braces. This was done so that any BibTeX interpreter would not convert initials to lowercase as if they were a full name. Thus, the field entry is "author = {{ML Nelson} and {MC Weigle} and {SM Jones}}" here. (2) A comma is provided at the end of every entry even though this is not required as it provided better identification if added fields are appended. The output includes line breaks and indents to facilitate a user scanning the results. 

### createhtml

The createhtml() function imports the ORS entries and converts them to an HTML style list. Because HTML files require lines of code before and after a list to identify document type, style, title, head, and body, the function is more involved than the other functions. The program does not currently use a specified style, but the line in the code remains, being commented out, so that a user can easily include that functionality. Additionally, the program allows the user to specify the title for the webpage if desired using the optional "--title" argument with a subsequent title. All list entries are enclosed within < ol > tags to identify them as an ordered list. Because of the structure of HTML code, line breaks and indents are NOT included within individual entries. 


### orsconvert.py examples

The following is an example of the orsconvert.py program converting an ORS entry into JSON format:

```
$ ./orsconvert.py --json XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.ors
2990027422b3de81a5abf997c5c94c18 2018
{     
     "DirectURL": "https://scholar.google.com/citations?view_op=view_citation&hl=en&oe=ASCII&user=QjHw7ugAAAAJ&pagesize=100&sortby=pubdate&citation_for_view=QjHw7ugAAAAJ:2osOgNQ5qMEC",
     "Title": "How perceptions of web resource boundaries differ for institutional and personal archives",
     "Authors": [
     "F Poursardar",
     "F Shipman"
     ],
     "Source": "2018 IEEE international conference on information reuse and integration (iri …, 2018",
     "CitedBy": "https://scholar.google.com/scholar?oi=bibs&hl=en&oe=ASCII&cites=10120194878620841447",
     "Citations": 4,
     "PageYear": 2018
}     
$                                                                                                                        
```

The following is an example of the orsconvert.py program converting an ORS entry into BibTeX format:

```
$ ./orsconvert.py --bibtex XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.ors
@misc{2990027422b3de81a5abf997c5c94c18:2018,
     title = {How perceptions of web resource boundaries differ for institutional and personal archives},
     author = {{F Poursardar} and {F Shipman}},
     date = {2018},
     howpublished = {2018 IEEE international conference on information reuse and integration (iri …, 2018},
     url = {https://scholar.google.com/citations?view_op=view_citation&hl=en&oe=ASCII&user=QjHw7ugAAAAJ&pagesize=100&sortby=pubdate&citation_for_view=QjHw7ugAAAAJ:2osOgNQ5qMEC},
},   
$                                                                                                                       
```

The following is an example of the orsconvert.py program converting an ORS entry into HTML format: 


```
$ ./orsconvert.py --html --title "Article Results" XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-08-04-0000-0099.ors
<html>
<head>
<title>Article Results</title>
<body bgcolor="white">
<h2>Article Results</h2>
<p> </p>
<ol>
<li>F Poursardar, F Shipman, <b><a href="https://scholar.google.com/citations?view_op=view_citation&hl=en&oe=ASCII&user=QjHw7ugAAAAJ&pagesize=100&sortby=pubdate&citation_for_view=QjHw7ugAAAAJ:2osOgNQ5qMEC">How perceptions of web resource boundaries differ for institutional and personal archives</a></b>, 2018 IEEE international conference on information reuse and integration (iri …, 2018.<p> </p></li>
</ol>
</body>
</html> 
$  
```

You also have an option of HTML structures, for example using --html2:

```
 ./orsconvert.py --html2 --title "Article Results" comprehensive.ors > results.html
```

The final solution is a converted comprehensive list of results that can be saved as a file specified by the user:

```
$ ./orsconvert.py --html --title "Article Results" comprehensive.ors > results.html
```

### orsconvert.py sorting by year

Articles may be sorted by a specified range using the command line argument --sort "x-y":

```
./orsconvert.py --html --sort "2010-2015" --title "Article Results" comprehensive.ors > all.html
```
Specifying only a start year will give you results up to most recent:

```
./orsconvert.py --html --sort "2010" --title "Article Results" comprehensive.ors > all.html
```

### orsconvert.py caveats

The orsconvert.py program processes basic entries within an ORS file. As much as possible, it distinguishes the fields according to what has been saved from the HTML page and converted by the html2ors.py program. However, the process is limited by the accuracy of each step according to the information provided by Google Scholar. The program was designed to recognize certain uncommon entries in the fields in the GS webpage, such as quotation marks in titles or missing entries in sources, but unexpected entries may result in the program incorrectly processing information. 

## Disclaimer

These programs are not guaranteed to operate with 100% accuracy in all conditions, so the developer maintains no liability.

  
  

