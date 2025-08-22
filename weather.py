from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

s = HTMLSession()
months = ['january', 'february', 'march', 'april', 'may']
sub = { 'january': '1', 'february' : '2', 'march' : '3', 'april' : '4', 'may': '5', 'june': 6
}
years = [2024]
# url = 'https://www.accuweather.com/en/vn/buon-ma-thuot/352955/{}-weather/352955?year={}'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'}


# r = requests.get(url)
# print(r)
def scraping(months, years, header):
    time = []
    temp = []
    for year in years:
        for month in months:
            start = 0
            end = 0
            url = f'https://www.accuweather.com/en/vn/buon-ma-thuot/352955/{month}-weather/352955?year={year}'
            r = s.get(url, headers=header)
            soup = BeautifulSoup(r.text, "lxml")
            date = soup.find_all("div", class_="date")
            high = soup.find_all("div", class_="high")
            low = soup.find_all("div", class_="low")
            dates = []
            temperature = []
            for d in date:
                dates.append(d.text.strip())
            for i in range(len(high)):
                h = high[i].text.strip()[:-1]
                l = low[i].text.strip()[:-1]
                temperature.append((float(h) + float(l)) / 2)
            start = dates.index('1')
            end = (dates[start + 1:].index('1') + start + 1) //2 + 3
            time  += [i + f'/{sub[month]}' + f'/{year}' for i in dates[start : end]]
            temp += temperature[start: end]
    return time, temp

time, temperature = scraping(['june'], years, header)
# print(time)
# print(temperature)
data = dict({"Date" : time, "Temperature" : temperature})
df = pd.DataFrame(data)
df.to_csv("weather_test.csv")

