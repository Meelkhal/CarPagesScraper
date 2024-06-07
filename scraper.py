# WEB SCRAPING LIBRARIES
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# SQL LIBRARIES
import sqlite3
import sqlalchemy

# DATA SCIENCE LIBRARIES
import pandas as pd

# IMPORTING UTILS
import scrapers.carpages as CP
import scrapers.autotrader as AT

class carScraper:

    def __init__(self,webDriver,page):
        self.webDriver = webDriver
        self.page = page

        # This directory is needed to convert the body type to the corresponding code for carpages.ca, this is needed to make sure that
        # we can acesses the carpages.ca website by code
        self.carPageDictionary = {"convertible" : 1,
                                 "coupe" : 2,
                                 "hatchback" : 3,
                                 "minivan" : 4,
                                 "sedan" : 5,
                                 "suv" : 6,
                                 "truck": 7,
                                 "wagon" : 8,
                                 "other" : 9,
                                 "commerical" : 10,
                                 "motorcycle": 11,
                                 "rv" : 12,
                                 "boat": 13,
                                 "trailer": 14}

        # A list containing the page data for each website 
        self.pageData = []

    def changePage(self,newPage):
        # Allows the user to change to scraping a new page
        self.page = newPage

    def changeBrowser(self,newBrowser):
        # Allows the user to change to scraping with a new browser
        self.browser = newBrowser

    def extractHtmlData(self,bodyType,numPages):
        # Extracts numpages worth of html source data for the webpages
        self.numPages = numPages
        self.bodyType = bodyType
        
        service = Service(executable_path=self.webDriver)
        driver = webdriver.Chrome(service=service)

        if self.page == "autotrader":
            website = "https://www.autotrader.ca/"+bodyType+"/"
        elif self.page == "carpages":
            website = "https://www.carpages.ca/used-cars/search/?num_results=50&category_id="+str(self.carPageDictionary[bodyType])+"&p=1"
        
        driver.get(website)

        for i in range(0,numPages):
            html = driver.page_source
            self.pageData.append(html)

            if self.page == "autotrader":
                button_elements = driver.find_element(By.CLASS_NAME,"last-page-link")
            elif self.page == "carpages":
                button_elements = driver.find_elements(By.CLASS_NAME,"nextprev")[-1]
            button_elements.click()

        driver.quit()

    def getPageData(self):
        # Obtains the listing data from the html sources and converts it into a pandas dataframe

        if self.page == "carpages":
            self.data = CP.scrapePageData(self.bodyType,self.pageData)

        elif self.page == "autotrader":
            self.data = AT.scrapePageData(self.bodyType,self.pageData)

    def savetoCsv(self,name):
        # Saves the data to a csv file
        self.data.to_csv(name)

    def savetoXlsx(self,name):
        # Saves the data to an excel file
        self.data.to_excel(name)

