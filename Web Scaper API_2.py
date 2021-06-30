from bs4 import BeautifulSoup
import requests
import csv

payload = {"ADDRESS": "1458 26th AVE NE"`}
source = requests.get("https://gismaps.kingcounty.gov/parcelviewer2/", params=payload)
if (source.status_code 1= 200):
  csv_writer("Error")
else:
  source.json
