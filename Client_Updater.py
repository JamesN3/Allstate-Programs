# Author: James Ngai(Allstate "HALE INSURANCE, INC.")
# Program built solely for the use of Allstate Hale Insurance Inc
#
# Program takes prexisting client data and adds the client's
# Housing Square Footage(Potentially), Present Use, and property detail url

import requests
import csv
import concurrent.futures
import pandas as pd
from os import path
from bs4 import BeautifulSoup

# Message is to inform user about program operations
print(
    "\nOutput file will be in same folder as input file\nNew file name will be "
    "new_{file_name}.csv"
    ""
)

# Takes the PATH of the csv file
PATH = str(
    input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
)

# Checks if file path exists and waits until user inputs correct one
while not path.exists(PATH):
    print("Error with file path, check it is correct and compare with example")
    PATH = str(
        input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
    )

# Reminder to ensure program does not stop in executiomn
print("Reminder: Do not open the csv file that is being read or written!")
# Pandas dataframa reads address_list to pass to threads
df = pd.read_csv(PATH)
address_list = df["Address"].tolist()
# Creates new file path for csv file that is being written
last_index = PATH.rfind("\\")
new_PATH = PATH[0 : last_index + 1] + "new_" + PATH[last_index + 1 :]
print(len(address_list))
# Main function that is called to determine the bar that should be set
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


# Counts the number of clients that fit within square_bar to determine bar to set to
def square_limit(square_bar):
    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        num_square_ft = 0
        for line in csv_reader:
            if int(line[8]) <= square_bar:
                num_square_ft += 1
    return num_square_ft


# Returns if the boolean if clients fit within limit
def square_bar_test(square_bar):
    if square_limit(square_bar) < 999:
        return True
    else:
        return False


# The message that is sent when an error occurs
error_message = "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"
# Calls function to get bar to set to
square_bar = square_call(square_bar=1800)

# Function that threads use
def add_list(address, row_val):
    # Bar to determine which clients should access the housing square footage data
    global square_bar

    # Opens new reader object for each thread
    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        # Iterates to the correct row to read from
        for _ in range(row_val):
            next(csv_reader)
        # Takes line that is going to be read from
        line = next(csv_reader)
        # Take address and converts to search friendly form
        # Converts spaces " " to "%20"
        address = address.replace(" ", "%20")
        try:
            # Takes pin_id or parcel number required to access web data and urls
            pin_id = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            ).json()["items"][0]["PIN"]
            # Takes present_use data Ex:"Single Family(Res)" to put in csv file
            present_use = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
            ).json()["items"][0]["PRESENTUSE"]
            if present_use == "":
                present_use = "Not Avaliable"
            # Creates url based off of pin_id(Parcel Number)
            # Url is not verified to avoid web visit restriction
            url = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
            # Signifies that process was successful to move onto access square footage data
        except:
            address = address.lower()
            # Dictionary that is circled through to see if search result can be recovered
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
            # Means process has failed thus far unless dictionary change finds search result
            passthrough = False
            # Loops through dictionary to see if dictionary result is in address
            for abbreviation, full in abb_dict.items():
                # Sees if results is in address and will fix search result and the computer well tell computer
                if f"%20{abbreviation}%20" in address:
                    address = address.replace(abbreviation, full)
                    passthrough = True
            # If dictionary element changed, the program will submit another request for data to fix field
            if passthrough:
                try:
                    pin_id = requests.get(
                        f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
                    ).json()["items"][0]["PIN"]
                    present_use = requests.get(
                        f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
                    ).json()["items"][0]["PRESENTUSE"]
                    url = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
                except:
                    line.append(error_message)
                    return line
            else:
                line.append(error_message)
                return line
        # Takes square_ft data from clients
        square_ft = int(line[8])
        if square_ft <= square_bar:
            if (
                "condo" not in present_use.lower()
                or "apartment" not in present_use.lower()
                or "mobile home" not in present_use.lower()
            ):
                try:
                    # Takes request for square footage
                    source = requests.get(
                        f"https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={pin_id}"
                    ).text
                    # Takes text element using Beautfiul Soup
                    soup = BeautifulSoup(source, "lxml")
                    # Parses through html to find correct source
                    table1 = soup.find("table", id="container")
                    table2 = table1.find("table", id="cphContent_DetailsViewPropTypeR")
                    tr = table2.find_all("tr")[1]
                    try:
                        header = tr.find_all("td")[0].text.lower()
                        if header == "total square footage":
                            new_square_ft = tr.find_all("td")[1].text
                        else:
                            new_square_ft = "Error"
                    except:
                        # Loops through tr tags in table
                        for value in tr:
                            try:
                                header = tr.find_all("td")[0].text.lower()
                                # Sees if header is correct then will append
                                if header == "total square footage":
                                    new_square_ft = tr.find_all("td")[1].text
                                    break
                            except:
                                new_square_ft = "-Error-"
                except:
                    # Inputs error message if previous proccesses failed
                    new_square_ft = "-Error-"
                # Appends square footage
                line.append(str(new_square_ft))
            else:
                # Appends dashes to maintain csv structure
                line.append("---")
        else:
            # Appends dashes to maintain csv structure
            line.append("---")
        # Appends previous information scraped
        line.append(present_use)
        line.append(url)
        return line


# Creates tuple to ensure each csv row is read for the correct row being written
num_list = tuple(range(1, len(address_list) + 1))
# Reads csv file to copy top line of csv_file
with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(new_PATH, "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        # Adds additional elements to top row of csv data
        first_line.append("Real Square Footage")
        first_line.append("Present Use")
        first_line.append("URL")
        csv_writer.writerow(first_line)
        # Opens threading module
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Maps function ensure the threads called first are executed first
            for line in executor.map(add_list, address_list, num_list):
                csv_writer.writerow(line)
print("Finished!")