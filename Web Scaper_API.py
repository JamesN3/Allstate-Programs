from bs4 import BeautifulSoup
import requests
import csv

word = "1458 26th AVE NE"
word = word.replace(" ", "%")
payload = {"identifier": "OBJECTID", "add": word}
# Replace addition signs with modulo signs
source = requests.get(
    "https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?",
    params=payload,
)
print(source.url)

# https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin=3630200160
# "PROPNAME": {"Single Family Residence"}