from bs4 import BeautifulSoup
import requests
import csv

source = requests.get("https://gismaps.kingcounty.gov/parcelviewer2/")