import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

def webScraper(minYear,minMiles,amt,make,model):

    headers = {
        'user-agent': 'Chrome/78.0.3904.108',
    }

    URL = 'https://www.autotrader.ca/cars' + make + '/on/toronto/?rcp=' + amt + '&rcs=0&srt=4&yRng=' + minYear + '%2C&oRng=%2C'+ minMiles + '&prx=250&prv=Ontario&loc=A1A%201A1&trans=Automatic&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch'

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    carElems = soup.find_all('div', class_='col-xs-12 result-item')

    carInfo = [["carTitle", "carMake", "carModel", "carYear", "carPrice", "carMile"]]



    for carElems in carElems:
        data = carElems.h2.span.string.lstrip().split(" ",1)
        carYear = data[0]
        carTitle = data[1].split("\n",1)[0]
        carPrice = carElems.find('span', class_='price-amount').string.replace(",","").replace("$","")
        carMake = carTitle.split(" ")[0]
        carModel = carTitle.split(" ")[1]

        skip = 0

        try:
            carMileData = carElems.find('div', class_='kms').text.split(" ",2)
            carMile = carMileData[1].replace(",","")

        except:
            carMile = "No Mileage Data"
            carInfo.clear()
            skip = 1

        try:
            if carInfo[-1][4] > carPrice:
                carInfo.clear()
                skip = 1

        except:
            random = 1

        if skip == 0: 
            info = [carTitle, carMake, carModel, carYear, carPrice, carMile]
            carInfo.append(info)


    make = make.replace("/","")
    model = model.replace("/","")
    with open(str(datetime.date(datetime.now())) + "_CarSearch_" + make + model + minYear +".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(carInfo)


minMiles = "125000"
amt = "30"

####Please ensure these two have slash's before word
''' <---------------------------------------------------- Place or remove "#" to change "mode"
make = "/volvo"
model = ""
minYear = "2015"
webScraper(minYear, minMiles, amt, make, model)


'''


####This makes a buncha shit

make = ["","/honda","/hyundai","/mazda","/volkswagen"]
model = ""
minYear = ["2014","2015","2016","2017","2018"]

for x in make:
    for i in minYear:
        webScraper(i, minMiles, amt, x, model)


#'''<---------------------------------------------------- and here Place or remove "#" to change "mode" 