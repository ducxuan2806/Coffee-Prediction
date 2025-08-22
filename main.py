import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

data = pd.read_csv("data_coffee.csv")
print(data.dtypes)
date = pd.to_datetime(data["Date"], format='%d/%m/%Y')
temp = data["Temperature"]
gas = data["Gas_Price"]
oil = data["Oil_Price"]
coffee = data["Coffee_price"]
plt.figure(figsize=(10, 5))
line1 = plt.plot(date, gas, color = 'r', label = 'gas')
line2 = plt.plot(date, temp, color = 'b', label = 'temp')
line3 = plt.plot(date, oil, color = 'g', label = 'oil')
line4 = plt.plot(date, coffee, color = 'y', label = 'coffee')
plt.xlabel("Date")
plt.xlim(pd.to_datetime(["1/1/2024", "31/5/2024"], format='%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.ylabel("Price")
plt.show()

