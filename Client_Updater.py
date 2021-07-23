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

print("Reminder: Do not open the csv file that is being read or written!")

df = pd.read_csv(PATH)
address_list = df["Address"].tolist()
last_index = PATH.rfind("\\")
new_PATH = PATH[0 : last_index + 1] + "new_" + PATH[last_index + 1 :]


def square_call(square_bar=1800):
    num_square_ft = square_limit(square_bar)
    if num_square_ft < 999:
        stopper = square_bar_test(square_bar + 10)
        if not stopper:
            return square_bar
        return square_call(square_bar + 10)
    else:
        stopper = square_bar_test(square_bar - 10)
        if stopper:
            return square_bar - 10
        return square_call(square_bar - 10)


def square_limit(square_bar):
    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        num_square_ft = 0
        for line in csv_reader:
            if int(line[8]) <= square_bar:
                num_square_ft += 1
    return num_square_ft


def square_bar_test(square_bar):
    if square_limit(square_bar) < 999:
        return True
    else:
        return False


error_message = "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
square_bar = square_call(square_bar=1800)


def add_list(address, row_val):
    global square_bar

    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in range(row_val):
            next(csv_reader)
        line = next(csv_reader)
        address = address.replace(" ", "%20")
        square_ft = int(line[8])
        try:
            pin_id = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            ).json()["items"][0]["PIN"]
            present_use = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
            ).json()["items"][0]["PRESENTUSE"]
            url = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
            passthrough = True
        except:
            address = address.lower()
            passthrough = False
            abb_dict = {
                "mt": "mountain",
                "mount": "mt",
                "woodinvl": "woodinville",
                "sunbreak": "sun break",
                "shr": "shore",
                "cntry": "country",
                "clb": "club",
                "lk": "lake",
                "shangrila": "shangri la",
                "shoreclub": "shore club",
            }
            for abbreviation, full in abb_dict.items():
                if f"%20{abbreviation}%20" in address:
                    address = address.replace(abbreviation, full)
                    passthrough = True
            if passthrough:
                pin_id = requests.get(
                    f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
                ).json()["items"][0]["PIN"]
                present_use = requests.get(
                    f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
                ).json()["items"][0]["PRESENTUSE"]
                url = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
            else:
                line.append(error_message)
                return line
        if passthrough:
            if square_ft <= square_bar:
                try:
                    source = requests.get(
                        f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
                    ).text
                    soup = BeautifulSoup(source, "lxml")
                    # Is it in TABLE1
                    table1 = soup.find("table", id="TABLE1")
                    table2 = table1.find_all("table", class_="GridViewStyle")[13]
                    tr = table2.find_all("tr")
                    for value in tr:
                        tester = value.find_all("td")[0].text.lower()
                        print(tester)
                        if tester == "avg unit size" or tester == "total finished area":
                            header = value.find_all("td")[0].text
                            new_square_ft = value.find_all("td")[1].text

                except:
                    new_square_ft = "-Error-"
                    header = "Error"
                line.append(str(new_square_ft))
            else:
                line.append("---")
        line.append(present_use)
        line.append(url)
        return line


num_list = list(range(1, len(address_list) + 1))
with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(new_PATH, "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        first_line.append("Real Square Footage")
        first_line.append("Present Use")
        first_line.append("URL")
        csv_writer.writerow(first_line)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for line in executor.map(add_list, address_list, num_list):
                csv_writer.writerow(line)
print("Finished!")