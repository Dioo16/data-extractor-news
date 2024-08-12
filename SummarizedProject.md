# data-extractor-news
 bot for purposes of process automation.


				Code Challenging
							
						
						
## Purpose: 
Build a bot to process automation(Automate the tedious part of a process)

## What?: 
Extracting data from a news site

## Where: 
Push the code in a PUBLIC GITHUB REPOSITORY, and use it to create a robocorp control room process.(https://robocorp.com/docs/courses/beginners-course-python/12-running-in-robocorp-cloud)
## Tips:
   * Make sure to write your files to the /output directory so that they are visible in the artifacts list
   * Once Completed invite Challenges@thoughtfulautomation.com to your Robocorp Org.
		   
		   
## From: Any of these sites(choose the better)
	https://apnews.com/
	https://www.aljazeera.com/
	https://www.reuters.com/
	https://gothamist.com/
	https://www.latimes.com/
	https://news.yahoo.com/


## Parameters(to search from robocloud):
 * search phrase
 * news category/section/topic
 * number of months for which you need to receive news (if applicable)
		            
       Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on

  These may be defined within a configuration file, but we’d prefer they be provided via a Robocloud workitem

## The process(not automated)     


1) Open the site by following the link

2) Enter a phrase in the search field

3) On the result page, If possible select a news category or section from the  
 Choose the latest (i.e., newest) news

 4) Get the values: title, date, and description.
 
 5) Store in an Excel file:
 
    *  title
    *  date
    *  description (if available)
    * picture filename
    * count of search phrases in the title and description
    * True or False, depending on whether the title or description contains any amount of money
    Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

6) Download the news picture and specify the file name in the Excel file

7) Follow steps 4-6 for all news that falls within the required time period



____________________________

# Parameters of avaliability

1) Quality code Your code is clean, maintainable, and well-architected. The use of an object-oriented model is preferred.
We would advise you ensure your work is PEP8 compliant
Employ OOP

2) Resiliency Your architecture is fault-tolerant and can handle failures both at the application level and website level.
Such as using explicit waits even when using the robocorp wrapper browser for selenium

3) Best practices Your implementation follows best RPA practices.
Use proper logging or a suitable third party library
Use appropriate string formatting in your logs (note we use python 3.8+)


___________________________

# Rules

Do NOT use APIs or Web Requests for this exercise!!
Please leverage pure Python

1) Please use pure Python (as demonstrated here) and pure Selenium (via rpaframework: https://rpaframework.org/ ) without utilizing Robot Framework.

2) An example of using Selenium directly from rpaframework can be found here. You can use either the CustomSelenium or ExtendedSelenium approach: https://github.com/robocorp/ways-of-webdrivers

