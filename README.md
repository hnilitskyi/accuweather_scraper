Accuweather scraper

Project aims to collect data on hurricanes from a specified start year to a specified end year from the Accuweather website. It includes information such as the start date, end date, and characteristics of each hurricane, and saves it into an Excel file (XLS) for further analysis.

     Features
Dynamic Year Range: Users can specify the start and end years for data scraping, allowing for targeted extraction of hurricane data within a customizable time frame.
Web Scraping: The scraper utilizes BeautifulSoup and requests libraries to extract data from the Accuweather website. It collects essential information such as storm name, status, start date, start time, stop date, stop time, peak sustained winds, and peak wind gusts for each hurricane.
Data Formatting: Extracted data is formatted and organized into an Excel file (XLS) for easy access and further analysis. The Excel file includes designated columns for each data attribute, ensuring clarity and structure in the output.
     
     How to Use
Make sure to install:
BeautifulSoup4, requests, xlwt

To use the project, simply specify the start year and end year for data scraping in the provided Python script. Run the script, and it will automatically scrape the necessary data from Accuweather for each year within the specified range. 
The collected data is then organized and saved into an Excel file named "hurricanes_data.xls" for later analysis.
