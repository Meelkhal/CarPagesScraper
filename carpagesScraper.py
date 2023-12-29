from bs4 import BeautifulSoup
import requests
import pandas as pd

def getMileage(car):
    # Inputs:
    # car(List) - List of tags for a one car listing on carpages.ca
    #
    # Outputs:
    # mileage(int/str) - mileage as string or integer
    #
    # Purpose:
    # Gets the mileage of one car listing
    mileage = ""
    mileageInfo = car.findAll("div",class_="t-col-span-full mobile-lg:t-col-span-6 laptop:t-col-span-4")[0].find_all("span")
    for m in mileageInfo:
        mileage += m.text
    try:
        mileage = int(mileage.replace(",","")[0:-2])
    except ValueError:
        # Sometimes posters will put text in place of a mileage so we need to account for error handling using a try statement 
        pass

    return mileage

def getPrice(car):
    # Inputs:
    # car(List) - List of tags for a one car listing on carpages.ca
    #
    # Outputs:
    # price(int/str) - price as string or integer
    #
    # Purpose:
    # Gets the price of one car listing
    price = list(filter(lambda a: a != "",str(car.find("span").text).split(" ")))[-1] 
    price = price[1:len(price)]
    price = price.replace(",","")
    try:
        price = float(price)
    except:
        ValueError
    return price

def ExtractPageData(website,bodyType):
    # Inputs:
    # website(str) - website of carpages.ca 
    # bodyType(int) - bodyType of vehicle based off of carpages.ca's indices as defined below in bodyTypes dict
    # 
    # Outputs:
    # pageData(pd) - pandas dataframe corresponding to all of the data saved for a carpages.ca listing
    #
    # Purpose:
    # Extracts all the car data on a given webpage  
    bodyTypes = {
        1:"Convertable",
        2:"Coupe",
        3:"Hatchback",
        4:"Hybrid/Electric",
        5:"Sedan",
        6:"SUV",
        7:"Crossover",
        8:"Van/Minivan",
        9:"Pickup Truck"}

    response = requests.get(website)
    status = response.status_code
    soup = BeautifulSoup(response.content,'html.parser')

    # desired fields as dictionary
    data = {
        "Titles" : [],
        "Year" : [],
        "Model" : [],
        "Make" : [],
        "Colour" : [],
        "Style" : bodyTypes[bodyType],
        "Condition" : [],
        "Price" : [],
        "Mileages" : [],
        "Dealer" : [],
        "City": [],
        "Province" : [],
        "Posting Link": [],
        "Image Link": [],
    }
    soup = BeautifulSoup(response.content,'html.parser')
    cars = soup.find_all('div', class_='t-flex t-gap-6 t-items-start t-p-6')

    # loop for every car on the webpage and append the values to the data dictionary above
    for car in cars:
        vec = car.findAll("a")
        title = vec[0].find("img").get("alt")
        info = title.split(" ")
        data["Titles"].append(title)
        data["Condition"].append(info[0])
        data["Year"].append(info[1])
        data["Make"].append(info[2])
        data["Model"].append(car.find_all("a")[1].text)
        data["Province"].append(car.findAll("p", class_="hN")[0].text.split(", ").pop(1))
        data["City"].append(car.findAll("p", class_="hN")[0].text.split(", ").pop(0))
        data["Dealer"].append(car.findAll("h5")[-1].text)
        data["Mileages"].append(getMileage(car))
        data["Price"].append(getPrice(car))
        data["Posting Link"].append("https://www.carpages.ca"+car.find("a").get("href"))
        data["Image Link"].append(car.find_all("a")[0].find("img").get("data-original"))
        data["Colour"].append(car.find("span",class_="t-text-sm t-font-bold").text)

    pageData = pd.DataFrame(data)
    return pageData

def ExtractPageRangeData(bodyType,currentPage,finalPage):
    # Inputs:
    # currentPage(int) - first page you wish to extract data from
    # finalPage(int) - last page you wish to extract data from
    # bodyType(int) - bodyType of vehicle based off of carpages.ca's indices (Sedan,SUV, etc...)
    # 
    # Outputs:
    # table(pd) - pandas dataframe corresponding to all of the data saved from carpages.ca between pages currentPage->finalPage for a vehicle of a body type 
    #
    # Purpose:
    # Extracts all the car data on a given webpage  
    tableOfData = []

    while currentPage <= finalPage:
        try:
            website = "https://www.carpages.ca/used-cars/search/?num_results=50&category_id="+str(bodyType)+"&p="+str(currentPage)
            tableOfData.append(ExtractPageData(website,bodyType))
            currentPage += 1
        except Exception:
            break

    table = pd.concat(tableOfData,ignore_index=True)
    return table


