import requests
import csv
import concurrent.futures
import pandas as pd
from os import path
from bs4 import BeautifulSoup


print(
    "\nOutput file will be in same folder as input file\nNew file name will be "
    "new_{file_name}.csv"
    ""
)

PATH = str(
    input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
)
while not path.exists(PATH):
    print("Error with file path, check it is correct and compare with example")
    PATH = str(
        input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
    )
pd_csv = pd.read_csv(PATH)
address_list = pd_csv["Address"].tolist()
last_index = PATH.rfind("\\")
new_PATH = PATH[0 : last_index + 1] + "new_" + PATH[last_index + 1 :]

row_val = 1

def square_call(square_bar):
    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
            num_square_ft = 0
            for line in csv_reader:
                if int(line[8]) <= square_bar:
                    num_square_ft += 1
            if (num_square_ft < 940):
                square_call(square_bar + 10)
            elif (num_square_ft >= 999):
                square_call(square_bar - 10)
            else:
                return square_bar
                
def square_call():
    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        square_bar = 1750
            num_square_ft = 0
            for line in csv_reader:
                if int(line[8]) <= square_bar:
                    num_square_ft += 1
            if (num_square_ft < 940):
                square_call(square_bar += 10)
            elif (num_square_ft >= 999):
                square_call(square_bar -= 10)
            else:
                return square_bar
            


def add_list(address):
    global row_val

    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in range(row_val):
            next(csv_reader)
        line = next(csv_reader)
        row_val += 1
        address = address.replace(" ", "%20")
        square_ft = int(line[8])
        try:
            source1 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            )
            pin_id = source1.json()["items"][0]["PIN"]
            source2 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
            ).json()["items"][0]["PRESENTUSE"]
            square_true = False
            if square_ft <= square_bar:
                try:
                    square_true = True
                    source3 = requests.get(
                        f"https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={pin_id}"
                    ).text
                    soup = BeautifulSoup(source3, "lxml")
                    table = soup.find_all("table", class_="GridViewStyle")[1]
                    tr = table.find("tr", class_="GridViewAlternatingRowStyle")
                    new_square_ft = tr.find_all("td")[1].text
                except:
                    new_square_ft = "Error"
            source4 = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
        except:
            line.append(
                "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
            )
            return line
        line.append(str(source2))
        if square_true:
            line.append(str(new_square_ft))
        line.append(str(source4))
        return line


with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(new_PATH, "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        first_line.append("Present Use")
        first_line.append("Real Square Footage")
        first_line.append("URL")
        csv_writer.writerow(first_line)
        square_bar = square_call()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for result in executor.map(add_list, address_list):
                csv_writer.writerow(result)
print("Finished!")
