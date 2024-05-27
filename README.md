# 🚗 CarScraper
 Project which scrapes car listing data from the websites [carpages.ca](https://carpages.ca/) and
 [autotrader.ca](https://www.autotrader.ca/)
 
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

## Ex.1 Getting sedan data from autotrader from the first 2 pages
```python
from scraper.py import *
scraper = carScraper("chromedriver.exe","autotrader")
scraper.extractHtmlData("sedan",2)
scraper.getPageData()
scraper.save_to_csv("data.csv")
```

### Ex.2 Getting sedan data from carpages.ca from the first 5 pages
```python
from scraper.py import *
scraper = carScraper("chromedriver.exe","carpages")
scraper.extractHtmlData("sedan",5)
scraper.getPageData()
scraper.save_to_csv("data.csv")
```
