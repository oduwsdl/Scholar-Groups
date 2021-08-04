# WSDL Google Scholar

The attached programs are designed to scrape specific pages from Google Scholar to extract a comprehensive list of articles, remove duplicate entries when multiple authors work on the same paper, and save the entries into a specified format. All programs were designed to operate from the Command Line Interface in a Bash shell. Although these programs are designed to work together, than can certainly be used individually. Currently, the 4 programs are 

[htmlsave.py](#htmlsave.py)

html2ors.py

dedup.py

orsconvert.py

Python was used as it was easier to coordinate it with the Command Line Interface as a scripting language. 


# htmlsave.py

The htmlsave.py program simply allows the user to enter specific author IDs for a Google Scholar page and, using those IDs, downloads the HTML pages associated with the author. The 'sys.argv' library function is used to capture the author IDs from the command line, and a loop allows the program to capture 100 articles at a time until all articles have been downloaded. This does 100 articles at a time and saves each webpage individually as its own file. 

$ ./htmlsave.py authorID1 authorID2 authorID3 ...

The program uses the requests.get function to obtain the HTML content. The status code is used to verify if a valid webpage has been received. If an invalid author ID is entered, a status code '404' is received, and the HTML page is not downloaded. A simple '302' redirect is allowed when the final page has the correct '200' status code. The one limitation is that the user must know the current author ID in order to download articles. In cases where an author's ID has been changed, the page will redirect in a way that gives a '302' redirect for users who are logged into the Google Scholar service but gives a '404' for unknown users. Because this program will not be recognized as a known user, it cannot capture the redirected page even when entering the URL in a browser would redirect successfully. However, successfully navigating a redirect for changed author IDs would not be useful because the new page shows only the first 20 articles irrespective of the range provided in the original URL link. Therefore, it is beneficial for the user to receive an error and be responsible for identifying the author's updated ID. Additionally, the program uses a while loop to capture additional pages of articles until it finds a specific qualifier string. The string ">There are no articles in this profile.<" is currently the qualifier to identify when all articles have been captured.


**html2ors.py**

The html2ors.py program uses Beautiful Soup to extract article contents from the previously downloaded HTML file. Elements are extracted on a line-by-line basis. Currently, the program runs from the Command Line Interface. The user must specify the name of the HTML file to convert to ORS type. The program can convert one or multiple HTML files. Additionally, the program saves the ORS file in the same naming convention as the name of the original HTML file, so it is relatively easy to identify which HTML files have been converted. 
The createfilename() function uses a specific ID separator of 'XXXXXXX' before and after the author ID value. Originally, the file would start with the author ID and have the date string appended to it. 

$ ./html2ors.py aBcD12DefGHIj 

However, some author IDs in Google Scholar will contain hyphens " - " and underscores " _ " that create significant errors when trying to process commands from the Command Line Interface. For example, one author in the WSDL group had an ID in the form "-eRx..." that was read as an optional argument in Linux. Prefacing it with \ would work with manually-entered commands, but this is not as easily implemented when using automated scripts. Therefore, a character separator string was added. Currently, a set of 7 'X's are used as that is unlikely to be seen in an actual author ID field. The date field is then added to identify when the content has been downloaded from Google Scholar. This provides a record to reflect changes to the website and content over time. The beginning and ending strings are used to capture a range of articles due to pagination issues where GS only displays some of the articles at any time. Originally, GS showed only a certain range of pages, then the code was revised to display all articles, then it reverted back to showing only a range of articles/page. The range identifier in the filename is now set to 4 digits to the possibility to capture from 0001 - 9999 articles. The decision to use 4 digits instead of 3 digits was to prepare for the possibility that any user had more than 999 articles listed. 

The createURL() function provides the format of the URL to be captured by the program.  Originally, this was within the main code. However, ongoing changes in the HTML code for the Google Scholar webpage made it necessary to revise the code. Having this as a separate function facilitates future changes to the URL to be captured.

The findinitiallink() function is used to search the saved HTML file for the URL for each article. Originally, this was simply included in the main code. However, Google Scholar had revised their code 3 weeks after the project began, which required this to be revised as well. This was now converted to a separate function so that it is easier to identify and revise as necessary. The function is currently set to capture the link according to either the previous GS coding or the current GS coding. It finds the link and returns it to the main program where it was called. 

The createpopupURL() function is used to create the link necessary to cause the GS article link to open the article in a popup window instead of just in a separate window. Originally, this was part of the main code but has been converted to a called function. It currently does not work as Google Scholar has removed that functionality from the webpage. However, the function has been left intact in case the ability again becomes available through the GS website.


**dedup.py**

This program examines entries in an ORS file to remove duplicates. The program is designed to take a filename as input or to read lines from the Command Line Interface. Currently, it displays unique entries using the STDOUT function. However, it can easily be revised to display those entries that are duplicates. The program functions by examining the first key in the ORS file, which is a hash of the title, and storing it in an array. After that first entry is stored, the hash key value is extracted from each line and compared with the array. If no duplicate entry is found, the line is sent to the STDOUT function, and the hash key is added to the array. If the hash is already found in the array, the link is skipped. 

$ ./dedup.py file1.ors file2.ors file3.ors > allfiles.ors


**orsconvert.py**

This program imports entries structured in a dictionary-type key/value format and converts the entries to JSON, BIBTEX, or HTML. The program is run from the Command Line Interface. It can read from STDIN or accept a designated file as input, and it can read to STDOUT or be redirected to a file. The Argparse library is imported to define and recognize arguments. Currently, --json, --bibtex, and --html are the three options for exported formats. Although convention indicates that "--" on the front of an argument makes it optional, these three formats are configured so that one argument is required, and only one may be selected. An optional "--title" argument is included so that the user may designate the title of the page; this is only useful when the --html option is selected. 

$ ./orsconvert.py --html --title "This is the page title" comprehensivefile.ors

The createjson() function is designed to import the ORS entries and convert them into a JSON recognized format. Normal JSON conventions are used, such as brackets [] for an array, and a space after the colon in the "Key": "Value" pairings. The function is separated from the main portion of code to facilitate any future need for revision. Currently, the function uses simple string replacement to extract and format the information. Originally, the attempt was made to parse the items with a dictionary library, but this created errors if quotation marks were part of a title, which was the case in at least one instance. For example, an article title of "Why are some files "lost" in the cloud?" would be identified as two fields instead of one. Because titles and source information listings often contain quotation marks and colons, it seemed that a dictionary parser was not a good choice. 

The createbibtex() function imports the ORS entries and converts them to BIBTEX format. In this case, all entries are specified as "@misc" types as there is no easy way to identify the actual type of entry from the often-abbreviated notation used by Google Scholar. There are two deviations from normal BIBTEX conventions: (1) Instead of only having one set of curly braces around all authors, each author is also in braces. This was done so that any BIBTEX interpreter would not convert initials to lowercase as if they were a full name. Thus, the field entry is "author = {{ML Nelson} and {MC Weigle} and {SM Jones}}" here. (2) A comma is provided at the end of every entry even though this is not required as it provided better identification if added fields are appended. 

The createhtml() function imports the ORS entries and converts them to an HTML style list. Because HTML files require lines of code before and after a list to identify document type, style, title, head, and body, the function is more involved than the other functions. The program does not currently use a specified style, but the line in the code remains, being commented out, so that a user can easily include that functionality. Additionally, the program allows the user to specify the title for the webpage if desired using the optional "--title" argument with a subsequent title. All list entries are enclosed within <ol> tags to identify them as an ordered list. 

