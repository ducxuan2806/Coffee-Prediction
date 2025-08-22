from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

k = 20 #k đây là số page muốn lấy
brsd = [i * 10 for i in range(k)] # tập id các page
print(brsd)
s = HTMLSession()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'}

def getlink(brsd, header): #Lấy link từ các page . Bởi vì 1 page có nhiều bài viết và mỗi bài viết dẫn đến các link khác nhau
    link = [] #lấy link từ html
    date = [] #lấy thời gian từ link
    for nb in brsd:
        url = f'https://congthuong.vn/chu-de/gia-ca-phe-trong-nuoc.topic&s_cond=&BRSR={nb}' #đặt url
        r = s.get(url, headers=header) #dùng bs4 để truy cập vào url
        soup = BeautifulSoup(r.text, 'lxml')
        data = soup.find_all("a")  # link có trong header "a"

        for article in data:
            title = article.get_text('title') # Lấy các tiêu đề trên các link này
            if "Giá cà phê hôm nay" in title: # Các này tiêu đề bài viết mọi người có thể tự config lại tùy ý. Tại mình muốn lấy trong những bài viết có tiêu đề này nên sẽ để text có trong tiêu đề tương ứng
                link.append(article.get('href')) #Lấy link
                titlelist= title.replace(":","").strip().split() #Cắt link này thành 1 tập list để có thể dễ lấy các ngày có trong dữ liệu hơn
                print(titlelist)
                date.append(titlelist[5]) # Index trong titlelist là vị trí chứa thời gian
    return link[1: ], date[1 : ]

link, date = getlink(brsd, header)
print(len(link))
print(date)

def getprice(text): #Lấy giá, bởi vì có 2 giá nên mình sẽ lấy giá trung bình cho dễ
    liststr = text.replace(".", "").split("đồng/kg") # dùng "đồng/kg" làm địa chỉ để lấy giá để tách thành list
    priceone = float(liststr[0].split()[-1]) # Tạo list mới từ 2 list được tạo thành bên trên rồi lấy thành phần cuối cùng để lấy giá
    pricetwo = float(liststr[1].split()[-1])
    return (priceone + pricetwo) / 2

def extract(link, date): # Trích xuất text để lấy giá
    price = []
    for index, l in enumerate(link):
        r = s.get(l, headers=header)  #Truy cập vào các bài viết có trong link
        soup = BeautifulSoup(r.text, 'lxml')
        data = soup.find_all("p") #Tìm tới header "p" đêr lấy dữ liệu
        for i in data:
            content = i.get_text()
            lc = content.split('/n') # Chặt thành 1 list các đoạn
            for i in lc: #Đoạn nào có chứa text này thì fill ngày tháng cần lấy tương ứng trong link lại rồi bắt đầu lấy giá
                if f"giá cà phê hôm nay (ngày {date[index].replace('/2024', '')}) tại tỉnh đắk lắk" in i.lower():
                    xau = i.replace(",", "") #Loại bỏ dấy "," giữa các câu
                    price.append(getprice(xau))

    return price

price = extract(link, date)
cost = price[::-1]
print(cost)
#Phần dưới dùng để fill các giá trị khuyết, nhưng cái này là từ lúc làm project rồi
# cost.insert(5, float(67700))
# cost.insert(6, float(68200))
# cost.insert(21, float(72450))
# cost.insert(106, float(113550))
cost.insert(4, 122950)
cost.pop(-1)
data = pd.read_csv("weather_test.csv")
data["coffee_price"] = cost #Cái này có thể lỗi tại lúc code này, mk thử nghiệm trên file test trước nên số lượng crawl không đủ với thời gian phải căn tương ứng
#với file được crawl từ file weather.csv

data.to_csv("data_coffee_test.csv")
