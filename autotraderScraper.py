from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import pandas as pd


def extractPages(bodyType="sedan",numPages=10):
    # Inputs:
    # numPages(int) - Number of pages we wish to extract HTML data from autotrader.ca
    # bodyType(str) - The bodytype of the vehicle we will interested in (Seda, suv, truck, etc)
    #
    # Outputs:
    # html_pages(list of html) - Returns list of size numpages containing HTML sourcepage data
    #
    # Purpose:
    # Extracts the html data from each of the pages
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.autotrader.ca/"+bodyType+"/")

    # Array storing which we use to store the contents of the scraped data in
    html_pages = []

    for i in range(numPages):

        html = driver.page_source
        html_pages.append(html)

        button_elements = driver.find_element(By.CLASS_NAME,"last-page-link")
        button_elements.click()

        time.sleep(2)

    driver.quit()

    return html_pages


def getPageData(bodyType="sedan",numPages=10):
    # Inputs:
    # numpages(int) - Number of pages we wish to extract HTML data from autotrader.ca
    #
    # Outputs:
    # html_pages(list of html) - Returns list of size numpages containing HTML sourcepage data
    #
    # Purpose:
    # Extracts the html data from each of the pages
    
    data = {
        "Titles" : [],
        "Year" : [],
        "Model" : [],
        "Make" : [],
        "Style" : bodyType,
        "Condition" : [],
        "Price" : [],
        "Mileages" : [],
        "City": [],
        "Province" : [],
        "Posting Link": [],
        "Image Link": [],
        "Source" : "autotrader.ca"}

    html_pages = extractPages(10)

    for html in html_pages:
        
        # For each page we extract the html contents and parse it in beautiful soup
        soup = BeautifulSoup(html, 'html.parser')

        cars = soup.find_all("a",class_="inner-link",href=True)
        
        # for since autotrader has two a tags with class_inner-link side by side, we must collect all of those tags and 
        # index by a step of 2 to prevent overcounting the vehicle data

        for index in range(0,len(cars),2):

            # Because how the individual car listing link is defined, we can get a lot of data from the link of the posting itself.
            # Ex.
            #  "https://www.autotrader.ca/a/nissan/sentra/mississauga/ontario/5_62080389_20100903134221117/?showcpo=ShowCpo&ncse=no&ursrc=ts&pc=N2B%202R1&sprx=100"
            # from this link for the following listing we can obtain that the car is a nissan sentra located in mississauga ontario.
            car_data = cars[index].attrs["href"].split("/") 
            make = car_data[2].replace("%20"," ")
            model = (car_data[2]+" "+car_data[3]).replace("%20"," ")
            city = car_data[4].replace("%20"," ").replace("%c3%a9","e")
            province = car_data[5].replace("%20"," ")

            # The price, condition, mileage are obtained using other tags
            price = int(cars[index+1].find_all(class_="price-amount")[0].get_text()[1:].replace(",",""))
            
            # By checking the condition of the car it also allows us to determine whether we can obtain the mileage
            # new cars have no mileage, thus they have mileage = 0
            condition = cars[index].find_all("p")[0].attrs["class"][1]
            if condition != "new":
                try:
                    mileage = cars[index].find("div",class_="margin-left-8").get_text().split(" ")[0].replace(",","")
                except Exception:
                    print(Exception,mileage)
                    mileage = None
            else:
                mileage = 0

            # Helpful the obtain the title of the listing. The title also allows us to obtain the year of the car listing
            title = cars[index].find_all("span",class_="title-with-trim")[0].get_text().strip("\n").strip(" ").strip("\n")
            year = int(title[0:4])

            # We obtain the full listing link, as well as the image link.
            listing_link = "https://www.autotrader.ca"+cars[index].attrs["href"]
            image_link = cars[index].find("img").get("data-original")

            # We append the scraped data to a dictionary
            data["Titles"].append(title)
            data["Year"].append(year)
            data["Model"].append(model)
            data["Make"].append(make)
            data["Condition"].append(condition)
            data["Price"].append(price)
            data["Mileages"].append(mileage)
            data["City"].append(city)
            data["Province"].append(province)
            data["Posting Link"].append(listing_link)
            data["Image Link"].append(image_link)

    # convert the dictionary to a pandas dataframe
    pageData = pd.DataFrame(data)
    return pageData
