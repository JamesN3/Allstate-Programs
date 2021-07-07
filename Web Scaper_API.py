import requests
import csv
import json


word = "1458 26th AVE NE"
word = word.replace(" ", "%")

source1 = requests.get(
    "https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add=1458%2026th%20ave%20NE"
)

pin_id = source1.json()["items"][0]["PIN"]


source2 = requests.get(
    f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
)

residence = source2.json()["items"][0]["PROPNAME"]
print(residence)