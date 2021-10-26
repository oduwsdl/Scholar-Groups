# Scholar Groups

<img src="/docs/gsflowdiagram.png" width="50%"><br />
Fig.1 Scholar Groups Process Flow

##<ins>Overview</ins>
Scholar Groups is a <ins>software toolkit</ins> developed in Python to extract scholarly literature from multiple authors using the Google Scholar search engine and grouping the results into a user specified order and format.

This document provides *"how-to"* instructions to get you started. Design notes can be found in the: <a href="/docs/designdoc.md">Design Document</a>.

The programs included in this toolkit are designed to work together:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 1**: *[htmlsave.py](README.md)* - For each Google Scholar ID, download paginated publication pages<br /><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 2**: *[html2ors.py](orsconvert.py)* -  parse article HTML contents and convert to .ors format<br /><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 3**: *[dedup.py](dedup.py)* -  remove duplicate entries when multiple authors work on the same paper<br/><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 4**: *[orsconvert.py](orsconvert.py)* - merge processed group of Google Scholar articles into a final report in a specified (JSON, BibTeX, or HTML) format 

Note: All programs operate from the Command Line Interface.

##Input : scholar.google.com
<img src="/docs/gs_input_example.png" width="40%"><br />
Fig.2 Author ID and Article Extraction
###Description:
The toolkit extracts the articles as input from the google scholar pages associated with the specified authors.



##STEP 1 : htmlsave.py

###Description:
The htmlsave.py program requires the user to enter specific author IDs for a Google Scholar page and using those IDs, downloads the HTML pages associated with the author. The program captures 100 articles at a time (server informed 100 page limit) for each ID and saves a webpage individually as its own file. 

###Example:
```
$ ./htmlsave.py oWQaPnwAAAAJ MOLPTqcAAAAJ OkEoChMAAAAJ -eRsYx8AAAAJ QjHw7ugAAAAJ Of8dNP0AAAAJ
Processing Author ID oWQaPnwAAAAJ ...
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.html"
Creating new file ...
File saved as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.html"
There are no more articles to capture ...
Processing Author ID MOLPTqcAAAAJ ...
Creating new file ...
File saved as "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.html"
Creating new file ...
File saved as "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.html"
There are no more articles to capture ...
Processing Author ID OkEoChMAAAAJ ...
Creating new file ...
File saved as "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.html"
There are no more articles to capture ...
Processing Author ID -eRsYx8AAAAJ ...
Creating new file ...
File saved as "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.html"
There are no more articles to capture ...
Processing Author ID QjHw7ugAAAAJ ...
Creating new file ...
File saved as "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.html"
There are no more articles to capture ...
Processing Author ID Of8dNP0AAAAJ ...
Creating new file ...
File saved as "XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.html"
There are no more articles to capture ...
$                                     
```
###Helpful Hints: 
The program will prompt a user when a new HTML file is overwriting another file of the same name, when an author ID is invalid, or when no further articles are available for download. 


##STEP 2 : html2ors.py

###Description:
The html2ors.py program parses the article content from the previously downloaded HTML files and converts the data to an <a href="https://github.com/oduwsdl/ORS/wiki/ORS">ORS </a>format. All ORS files generated use the same naming convention as the name of the original HTML file.

The ORS file consists of nine specific fields for each article entry:
1. Hash of title
2. Year of publication
3. DirectURL - URL to Google Scholar article
4. Title - Title of article
5. Authors - Authors associated with the article
6. Source - Main source of article according to GS
7. CitedBy - List of authors who have cited the article
8. Citations - Number of times the article has been cited in GS
9. PageYear - Year of publication

###Example:

```
$ ./html2ors.py *.html  
Importing "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.ors" ...
Importing "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.ors" ...
Importing "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.html" ...
Saving as "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.ors" ...
Importing "XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.ors" ...
Importing "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.ors" ...
Importing "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.ors" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.ors" ...
$     
```

### Helpful Hints:

If no file is listed after the executable, the program will prompt "No HTML files were identified for conversion". Some fields in the ORS entries may be blank, such as when an article has not been cited, or missing information. Because the program is capturing information from a Google Scholar page, all the data may not be listed. 


##STEP 3 : dedup.py
###Description:

The dedup.py program will analyze a large list of entries in multiple ORS files and remove duplicates. This is useful when compiling a database of articles by specific authors in which some articles are co-authored by members of the group. 

###Example:

```
$ ./dedup.py *ors > comprehensive.ors
$
$ wc *.ors
      90    3085   47966 XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.ors
     100    3011   51600 XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.ors
      91    2358   45117 XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.ors
      54    1861   29260 XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.ors
      60    1968   33383 XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.ors
       5     168    2846 XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.ors
     100    2887   51204 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.ors
     100    2752   52191 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.ors
     100    2720   53603 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.ors
     100    2696   53671 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.ors
     100    2441   50715 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.ors
      78    1806   37749 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.ors
     856   24363  447980 comprehensive.ors
    1834   52116  957285 total
$           
```
###Helpful Hints:
In the above example, all of the ORS files were processed and unique entries were stored in the "comprehensive.ors" file. The "wc" function shows the total number of entries before duplicates were removed (i.e., all ORS files excluding the comprehensive.ors file). This indicates there were duplicates.


The data in an ORS file can be sorted by "year of publication" and displayed in descending order by using a combination of the sort by key "-k", reverse results of comparison "-r", and "-n" compare according to string numerical value bash arguments as shown below.

```
$ ./dedup.py *ors | sort -k2 -rn > comprehensive.ors
$ 
```


##STEP 4 : orscovert.py

###Description:
The orsconvert.py program imports entries structured in a dictionary-type key/value format and converts the entries to JSON, BibTeX, or HTML. Currently, there are two ordered list formatting options for exporting HTML format using the --html2 argument. An optional "--title" argument is included so that the user may designate the title of the page; this is only used when the --html option is selected. An optional "--sort" argument is available to allow the user to sort articles by a specify a range of years, "start_year - end_year". The results are pipelined to a file specified by the user. 

### Converting ORS Examples:

* JSON format:

```
$ ./orsconvert.py --json comprehensive.ors > results.json                                                                                                                  
```

* BibTeX format:

```
$ ./orsconvert.py --bibtex comprehensive.ors > results.bib                                                                                                                         
```

* HTML format: 


```
$ ./orsconvert.py --html --title "Article Results"  comprehensive.ors > results.html
```

* Other HTML structure using --html2:
```
 ./orsconvert.py --html2 --title "Article Results" comprehensive.ors > results.html
```

#### Sorting by Year:

Articles may be sorted by a specified range of years using the command line argument --sort "x-y":

```
./orsconvert.py --html --sort "2010-2015" --title "Article Results" comprehensive.ors > all.html
```
Specifying only a start year will give you results up to most recent:

```
./orsconvert.py --html --sort "2010" --title "Article Results" comprehensive.ors > all.html
```
##Output : Merged_Results.html

<img src="/docs/output.png" width="50%"><br />
* The completely merged HTML file can be found <a href="">here</a>.

## Disclaimer:

The Scholar Groups toolkit scrapes Google Scholar, a service we do not control and it could change tomorrow.

  
  

