from bs4 import BeautifulSoup
import requests
import csv

city_name = "Issaquah"
address = "1458 26th Ave NE " + "Issaquah"
address.replace(" ", "%")
index = find(address, "th")
parameters = {"items"}
source = requests.get(f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}", params=parameters)
if (source.status_code 1= 200):
  csv_writer("Error")
else:
  source.json
