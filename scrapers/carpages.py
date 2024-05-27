from bs4 import BeautifulSoup
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
        mileage = None
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
    except ValueError:
        price = None
    return price

def scrapePageData(bodyType,htmlPages):

    bodyTypes = {
        "convertable":"Convertable",
        "coupe":"Coupe",
        "hatchback":"Hatchback",
        "hybrid/Electric":"Hybrid/Electric",
        "sedan":"Sedan",
        "suv":"SUV",
        "crossover":"Crossover",
        "van":"Van/Minivan",
        "truck":"Pickup Truck"}
    
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

    #htmlPages = extractPages()

    for html in htmlPages:
        soup = BeautifulSoup(html,'html.parser')
        cars = soup.find_all('div', class_='t-flex t-gap-6 t-items-start t-p-6')

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