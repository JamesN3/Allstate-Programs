import requests
import csv
import json


address = "910 NE High St, Issaquah, WA 98029"

address = address.replace(" ", "%20")

source1 = requests.get(
    f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
)

pin_id = source1.json()["items"][0]["PIN"]


source2 = requests.get(
    f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
)

residence = source2.json()["items"][0]["PROPNAME"]
print(residence)