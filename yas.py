import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

PATH = str(
    input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
)
pd_csv = pd.read_csv(PATH)
address_list = pd_csv["Address"].tolist()
for address in address_list:
    source1 = requests.get(
        f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
    )
    pin_id = source1.json()["items"][0]["PIN"]

    square_true = True
    source4 = requests.get(
        f"https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={pin_id}"
    ).text

    soup = BeautifulSoup(source4, "lxml")
    table = soup.find_all("table", class_="GridViewStyle")[1]

    tr = table.find("tr", class_="GridViewAlternatingRowStyle")

    new_square_ft = tr.find_all("td")[1].text
    print(new_square_ft)