# 🚗 CarScraper
 Project which scrapes car listing data from the website [carpages.ca](https://carpages.ca/) 
 
![image](https://github.com/Meelkhal/CarScraper/assets/52140659/5293f032-9c05-468b-bca0-62c64fd2cb1e)



# Requirements
Language

* `Python 3.X`
* 
Python Libraries
* `BeautifulSoup`
* `Pandas`
* `requests`

# How to Use

Save the `carpagesScraper.py` file and make sure that the above libraries with an appropriate version of python is installed.

### Ex.1 Getting data from the first page of a given body type

Carpages.ca indexes each body type of a vehicle with an integer known as the category_id

* 1 Convertable
* 2 Coupe
* 3 Hatchback
* 4 Hybrid/Electric
* 5 Sedan
* 6 SUV
* 7 Crossover
* 8 Van/Minivan
* 9 Pickup Truck

If I wanted to scrape all of the data on the first page of the sedan listings as a pandas dataframe, I would type the following command
```python
from carpagesScraper.py import *
currentPage = 1
bodyType = 5
dataTable = ExtractPageData(bodyType,currentPage)
```

### Ex.2 Getting data for a page range of a given body type
Lets say, I want all of the data between pages 1-10
```python
from carpagesScraper.py import *
bodyType = 5
currentPage = 1
finalPage = 10
dataTable = ExtractPageRangeData(bodyType,currentPage,finalPage)
```
