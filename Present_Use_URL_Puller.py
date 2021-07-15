import requests
import csv
import concurrent.futures
import pandas as pd

print("\nOutput file will be in same folder as input file")

file_path = str(
    input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
)
pd_csv = pd.read_csv(file_path)
last_index = file_path.rfind("\\")
print(last_index)
new_file_path = file_path[0 : last_index + 1] + "new_" + file_path[last_index + 1 :]
address_list = pd_csv["Address"].tolist()

row_val = 1

# C:/Users/jamie/Downloads/new_August2021.csv


def add_list(address):
    global row_val

    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in range(row_val):
            next(csv_reader)
        line = next(csv_reader)
        row_val += 1
        address = address.replace(" ", "%20")
        try:
            source1 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            )
            pin_id = source1.json()["items"][0]["PIN"]
            source2 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
            ).json()["items"][0]["PRESENTUSE"]
            source3 = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
        except:
            for _ in range(2):
                line.append(
                    "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
                )
            return line
        line.append(str(source2))
        line.append(str(source3))
        return line


with open(file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(new_file_path, "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        first_line.append("Present Use")
        first_line.append("URL")
        csv_writer.writerow(first_line)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for result in executor.map(add_list, address_list):
                csv_writer.writerow(result)