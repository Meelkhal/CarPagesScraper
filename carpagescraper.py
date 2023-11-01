def getMileage(car):
    # Takes a car and gives us the mileage from the tag
    unFilteredMileageTags = car.find("div",class_="grey l-column l-column--small-6 l-column--medium-4").find_all("span")
    mileage = ""
    for tag in unFilteredMileageTags:
        mileage += tag.text
    #mileage = int(mileage[0:2].replace(",",""))
    return mileage

def getLocationField(car):
    location = car.find("p").text
    city,province = location.split(" ")
    return city[0:-1],province

def parse_page(no_listings,body_type,page_num):
    # page_num is the page number
    # result_num is the number of the 
    website = "https://www.carpages.ca/used-cars/search/?num_results="+str(no_listings)+"&category_id="+str(body_type)+"&p="+str(page_num)
    response = requests.get(website)
    status = response.status_code

    titles,prices,links,mileages,dealers,locations = [],[],[],[],[],[]
    if status == 200:
        # this means we have the ability to scrape the website
        cars = soup.find_all('div', class_='media soft push-none rule')
        for car in cars:
            # We need to get the following data, title,price,link,mileage,dealer,location(city), location(province)
            title = car.find("a").get("title") # from the title (we can see if we can filter the model and the make from the )
            price = int(car.find("strong").text.strip().replace("$","").replace(",",""))
            link = "https://www.carpages.ca"+car.find("a").get("href")
            mileage = getMileage(car) # We make a function for the mileage as it takes some work
            dealer = car.find_all("h5")[1].text
            #city,province = getLocationField(car) # We make a similar function to parse the city and the province
            location = car.find("p").text

            titles.append(title)
            prices.append(price)
            links.append(link)
            mileages.append(mileage)
            dealers.append(dealer)
            locations.append(location)

    data_dict = {"titles":titles,"prices":prices,"links":links,"mileages":mileages,"dealers":dealers,"locations":location}
    data = pd.DataFrame(data_dict)
    return data