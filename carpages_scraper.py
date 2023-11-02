from bs4 import BeautifulSoup
import requests
import pandas as pd

def getMileage(car):
    # Takes a car and gives us the mileage from the tag
    unFilteredMileageTags = car.find("div",class_="grey l-column l-column--small-6 l-column--medium-4").find_all("span")
    mileage = ""
    for tag in unFilteredMileageTags:
        mileage += tag.text
   
    try:
        mileage = int(mileage[0:-2].replace(",",""))
    except ValueError:
        mileage = None
    return mileage

def getLocationField(car):
    location = car.find("p").text
    city,province = location[0:-4],location[-2:len(location)]
    return city,province

def getYearMake(car):
    # gets the year and make of the vehicle
    vehicle = car.find_all("a")[1].text
    year = int(vehicle[0:5])
    make = vehicle[5:len(vehicle)]
    return year,make

def parse_page(no_listings,body_type,page_num):
    # page_num is the page number
    # result_num is the number of the 
    styles = {
        "1":"Convertable",
        "2":"Coupe",
        "3":"Hatchback",
        "4":"Hybrid/Electric",
        "5":"Sedan",
        "6":"SUV",
        "7":"Crossover",
        "8":"Van/Minivan",
        "9":"Pickup Truck"}

    website = "https://www.carpages.ca/used-cars/search/?num_results="+str(no_listings)+"&category_id="+str(body_type)+"&p="+str(page_num)
    response = requests.get(website)
    status = response.status_code
    soup = BeautifulSoup(response.content,'html.parser')

    titles,prices,links,mileages,dealers,cities,provinces,years,makes = [],[],[],[],[],[],[],[],[]
    conditions = []
    if status == 200:
        # this means we have the ability to scrape the website
        cars = soup.find_all('div', class_='media soft push-none rule')
        for car in cars:
            # We need to get the following data, title,price,link,mileage,dealer,location(city), location(province)
            title = car.find("a").get("title") # from the title (we can see if we can filter the model and the make from the )
            condition = title[0:4]
            year,make = getYearMake(car)
            try:
                price = float(car.find("strong").text.strip().replace("$","").replace(",",""))
            except ValueError:
                price = None
            link = "https://www.carpages.ca"+car.find("a").get("href")
            mileage = getMileage(car) # We make a function for the mileage as it takes some work
            dealer = car.find_all("h5")[-1].text
            city,province = getLocationField(car) # We make a similar function to parse the city and the province
            location = car.find("p").text
            
            conditions.append(condition)
            years.append(year)
            makes.append(make)
            titles.append(title)
            prices.append(price)
            links.append(link)
            mileages.append(mileage)
            dealers.append(dealer)
            cities.append(city)
            provinces.append(province)

    data_dict = {"Titles":titles,"Year":years,"Model":makes,"Style":styles[body_type],"Condition":conditions,"Price":prices,"Link":links,"Mileages":mileages,"Dealer":dealers,"City":cities,"Province":provinces}
    data = pd.DataFrame(data_dict)
    return data