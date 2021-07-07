import requests
import csv


csv_name = str(input("Type in name of csv file\n"))

with open(f"C:/Users/jamie/Downloads/{csv_name}.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(f"C:/Users/jamie/Downloads/updated_{csv_name}.csv", "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        first_line.append("Present Use")
        csv_writer.writerow(first_line)
        for line in csv_reader:
            address = str(line[2])
            proper = True
            # Needs to be updated to work with more query searches
            address = address.replace(" ", "%20")
            try:
                source1 = requests.get(
                    f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
                )
                pin_id = source1.json()["items"][0]["PIN"]

                source2 = requests.get(
                    f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
                )
            except:
                proper = False
            if proper:
                residence = str(source2.json()["items"][0]["PRESENTUSE"])
                if residence == "":
                    residence = "Not Avaliable"
                line.append(residence)
                csv_writer.writerow(line)
            else:
                print(line)
                line.append("Not Avaliable")
                csv_writer.writerow(line)
