import requests
import csv
import concurrent.futures
import pandas as pd
from bs4 import BeautifulSoup
import time

csv_name = str(input("Type in name of csv file\n"))
pd_csv = pd.read_csv(f"C:/Users/jamie/Downloads/{csv_name}.csv")

address_list = pd_csv["Address"].tolist()

row_starter = int(input("Which row should we start reading from\n"))
row_val = row_starter


def add_list(address):
    global row_val
    global row_starter

    with open(f"C:/Users/jamie/Downloads/{csv_name}.csv", "r") as csv_file:
        csv_reader_1 = csv.reader(csv_file)
        next(csv_reader_1)
        for _ in range(row_val):
            next(csv_reader_1)
        line = next(csv_reader_1)
        if row_val - row_starter > 1000:
            time.sleep(60)
            exit()
        row_val += 1
        proper = True
        address = address.replace(" ", "%20")
        try:
            source1 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            )
            pin_id = source1.json()["items"][0]["PIN"]
            source2 = requests.get(
                f"https://www5.kingcounty.gov/kcgisreports/dd_report.aspx?PIN={pin_id}"
            ).text
            soup = BeautifulSoup(source2, "lxml")
            parcel = soup.find("span", id="DistrictsReportControl1_lblPIN").text
            source3 = requests.get(
                f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={parcel}"
            ).url
        except:
            proper = False
        if (
            proper
            and source3
            != "https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
        ):
            line.append(str(source3))
            return line
        elif (
            source3
            == "https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
        ):
            line.append(
                "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
            )
            return line
        elif (
            source3
            == "https://blue.kingcounty.com/Assessor/eRealProperty/ExceedCount.aspx"
        ):
            line.append(
                "Error(MAX DAILY) — Refer to https://blue.kingcounty.com/Assessor/eRealProperty/ExceedCount.aspx"
            )
            return line
        else:
            line.append(
                "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
            )
            return line


with open(f"C:/Users/jamie/Downloads/{csv_name}.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(f"C:/Users/jamie/Downloads/updated_URL_{csv_name}.csv", "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        first_line.append("URL")
        csv_writer.writerow(first_line)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for result in executor.map(add_list, address_list):
                csv_writer.writerow(result)