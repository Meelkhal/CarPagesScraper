# 🚗 CarScraper
 Project which scrapes car listing data from the websites [carpages.ca](https://carpages.ca/) and
 [autotrader.ca](https://www.autotrader.ca/)

# UPDATED 06-06-2024
* Created util which allows the user to save scrapped data to a .db file format
 
# UPDATED 05-27-2024
* Created scraper object from the carpages and autotrader scraper scripts

# Requirements
Language

* `Python 3.X`
* 
Python Libraries
* `Selenium`
* `BeautifulSoup`
* `Pandas`

# How to Use

Save the 'carscraper' directory and make sure that the above libraries with an appropriate version of python is installed.

## Ex.1 Getting sedan data from autotrader from the first 2 pages of the website and save it to the csv file "data.csv"
```python
from scraper import *
Scraper = carScraper("chromedriver.exe","autotrader")
Scraper.extractHtmlData("sedan",2)
Scraper.getPageData()
Scraper.savetoCsv("data.csv")
```

### Ex.2 Getting sedan data from carpages.ca from the first 5 pages of the website and save it to the csv file "data.csv"
```python
from scraper import *
Scraper = carScraper("chromedriver.exe","carpages")
Scraper.extractHtmlData("sedan",5)
Scraper.getPageData()
Scraper.savetoCsv("data.csv")
```
