# Scholar Groups

<img src="/docs/gsflowdiagram.png" width="50%"><br />
Fig.1 Scholar Groups Process Flow


## <ins>Overview</ins>
Scholar Groups is a <ins>software toolkit</ins> developed in Python to extract scholarly literature from multiple authors using the Google Scholar search engine and grouping the results into a user specified order and format.

This document provides *"how-to"* instructions to get you started. Design notes can be found in the: <a href="/docs/designdoc.md">Design Document</a>.

The programs included in this toolkit are designed to work together:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 1**: *[htmlsave.py](/code/htmlsave.py)* - For each Google Scholar ID, download paginated publication pages<br /><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 2**: *[html2ukvs.py](/code/ukvsconvert.py)* -  parse article HTML contents and convert to .ukvs format<br /><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 3**: *Sort* - remove duplicate entries when multiple authors work on the same paper<br/><br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**STEP 4**: *[ukvsconvert.py](/code/ukvsconvert.py)* - merge processed group of Google Scholar articles into a final report in a specified (JSON, BibTeX, or HTML) format 

Note: All programs operate from the Command Line Interface.

## Input : scholar.google.com
<img src="/docs/gs_input_example.png" width="40%"><br />
Fig.2 Author ID and Article Extraction
### Description:
The toolkit extracts the articles as input from the google scholar pages associated with the specified authors.



## STEP 1 : htmlsave.py

### Description:
The htmlsave.py program requires the user to enter specific author IDs for a Google Scholar page and using those IDs, downloads the HTML pages associated with the author. The program captures 100 articles at a time (server informed 100 page limit) for each ID and saves a webpage individually as its own file. 

### Example:
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
### Helpful Hints: 
The program will prompt a user when a new HTML file is overwriting another file of the same name, when an author ID is invalid, or when no further articles are available for download. 


## STEP 2 : html2ukvs.py

### Description:
The html2ukvs.py program parses the article content from the previously downloaded HTML files and converts the data to an <a href="https://github.com/oduwsdl/ORS/blob/master/ukvs.md">UKVS </a>format. All UKVS files generated use the same naming convention as the name of the original HTML file.

The UKVS file consists of nine specific fields for each article entry:
1. Hash of title
2. Year of publication
3. DirectURL - URL to Google Scholar article
4. Title - Title of article
5. Authors - Authors associated with the article
6. Source - Main source of article according to GS
7. CitedBy - List of authors who have cited the article
8. Citations - Number of times the article has been cited in GS
9. PageYear - Year of publication

### Example:

```
$ ./html2ukvs.py *.html  
Importing "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.ukvs" ...
Importing "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs" ...
Importing "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.html" ...
Saving as "XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.ukvs" ...
Importing "XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.ukvs" ...
Importing "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs" ...
Importing "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.ukvs" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.ukvs" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.ukvs" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.ukvs" ...
Importing "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.html" ...
Saving as "XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.ukvs" ...
$     
```

### Helpful Hints:

If no file is listed after the executable, the program will prompt "No HTML files were identified for conversion". Some fields in the UKVS entries may be blank, such as when an article has not been cited, or missing information. Because the program is capturing information from a Google Scholar page, all the data may not be listed. 


## STEP 3 : Sort Command
### Description:

The sort command ```cat *ukvs | sort -u -k1,1 | sort -k2 -rn > comprehensive.ukvs``` will analyze a large list of entries in multiple UKVS files and remove duplicates. This is useful when compiling a database of articles by specific authors in which some articles are co-authored by members of the group. 

### Example:

```
$ cat *ukvs | sort -u -k1,1 | sort -k2 -rn > comprehensive.ukvs
$
$ wc *.ukvs
      90    3085   47966 XXXXXXX-eRsYx8AAAAJXXXXXXX-2021-10-25-0000-0099.ukvs
     100    3011   51600 XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs
      91    2358   45117 XXXXXXXMOLPTqcAAAAJXXXXXXX-2021-10-25-0100-0199.ukvs
      54    1861   29260 XXXXXXXOf8dNP0AAAAJXXXXXXX-2021-10-25-0000-0099.ukvs
      60    1968   33383 XXXXXXXOkEoChMAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs
       5     168    2846 XXXXXXXQjHw7ugAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs
     100    2887   51204 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0000-0099.ukvs
     100    2752   52191 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0100-0199.ukvs
     100    2720   53603 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0200-0299.ukvs
     100    2696   53671 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0300-0399.ukvs
     100    2441   50715 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0400-0499.ukvs
      78    1806   37749 XXXXXXXoWQaPnwAAAAJXXXXXXX-2021-10-25-0500-0599.ukvs
     856   24363  447980 comprehensive.ukvs
    1834   52116  957285 total
$           
```
### Helpful Hints:
In the above example, all of the UKVS files were processed and unique entries were stored in the "comprehensive.ukvs" file. The "wc" function shows the total number of entries before duplicates were removed (i.e., all UKVS files excluding the comprehensive.ukvs file). This indicates there were duplicates.


The data in an UKVS file is sorted by "year of publication" and displayed in descending order by using a combination of the sort by key "-k", reverse results of comparison "-r", and "-n" compare according to string numerical value bash arguments.



## STEP 4 : ukvsconvert.py

### Description:
The ukvsconvert.py program imports entries structured in a dictionary-type key/value format and converts the entries to JSON, BibTeX, Markdown, or HTML. Currently, there are two ordered list formatting options for exporting HTML format using the --html2 argument. An optional "--title" argument is included so that the user may designate the title of the page; this is only used when the --html option is selected. An optional "--startyear,--endyear" argument is available to allow the user to sort articles by a specify a range of years. The results are pipelined to a file specified by the user.

### Converting UKVS Examples:

* JSON format:

```
$ ./ukvsconvert.py --json comprehensive.ukvs > results.json                                                                                                                  
```

* BibTeX format:

```
$ ./ukvsconvert.py --bibtex comprehensive.ukvs > results.bib                                                                                                                         
```
* Markdown format:

```
$ ./ukvsconvert.py --md --title "Article Results" comprehensive.ukvs > Merged_Results.md                                                                                                                         
```

* HTML format: 


```
$ ./ukvsconvert.py --html --title "Article Results"  comprehensive.ukvs > results.html
```

#### Sorting by Year:

Articles may be sorted by a specified range of years using the command line argument --startyear, --endyear:

```
./ukvsconvert.py --html --startyear "2010" --endyear "2021" --title "Article Results" comprehensive.ukvs > all.html
```
Specifying only a start or end year will give you the remaining results when an argument is missing:

```
./ukvsconvert.py --html --startyear "2010" --title "Article Results" comprehensive.ukvs > all.html
```
#### HTML List Format:

Articles may be formatted into different list types such as one list(1), seperate lists(all), or no list(none) by using the command line argument --list:

```
./ukvsconvert.py --html --startyear "2010" --endyear "2021" --list=all --title "Article Results" comprehensive.ukvs > all.html
```

## Output : Merged_Results.html

<img src="/docs/output.png" width="50%"><br />
* The completely merged HTML file can be found <a href="/docs/Merged_Results.html">here</a>.

## Disclaimer:

The Scholar Groups toolkit scrapes Google Scholar, a service we do not control and it could change tomorrow.

  
  

