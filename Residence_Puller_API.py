import requests
import csv
import json


csv_name = str(input("Type in name of csv file\n"))

with open(f"C:/Users/jamie/Downloads/{csv_name}.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    x = True
    first_line = next(csv_reader)
    with open(f"C:/Users/jamie/Downloads/updated_{csv_name}.csv", "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        first_line.append("Propname")
        csv_writer.writerow(first_line)
        for line in csv_reader:
            address = str(line[2])

            address = address.replace(" ", "%20")

            source1 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            )

            pin_id = source1.json()["items"][0]["PIN"]

            source2 = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
            )

            residence = str(source2.json()["items"][0]["PROPNAME"])
            print(line)
            line.append(residence)
            print(line)
            csv_writer.writerow(line)