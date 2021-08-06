# Author: James Ngai (Allstate "HALE INSURANCE, INC.")
# Program built solely for the use of Allstate Hale Insurance Inc
#
# Program takes prexisting client data and adds the client's
# Housing Square Footage(Potentially), Present Use, and property detail url

import requests
import csv
import concurrent.futures
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

# Creates new file path for csv file that is being written
last_index = PATH.rfind("\\")
new_PATH = f"{PATH[0 : last_index + 1]}new_{PATH[last_index + 1 :]}"


# The message that is sent when an error occurs
error_message = "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"


class Client:
    def __init__(self, line):
        self.first = line[0]
        self.last = line[1]
        self.address = line[2]
        self.city = line[3]
        self.zipcd = line[4]
        self.phone = line[5]
        self.homeyr = line[6]
        self.home_size = line[7]
        self.estimated_value = line[8]
        self.home_sale_date = line[9]
        self.mod_passthrough = False
        self.mod_first = ""
        self.mod_last = ""
        self.mod_sqft = ""
        self.mod_yr = ""
        self.mod_pres = ""
        self.mod_url = error_message
        self.mod_pin_id = ""

    def inital_packager(self):
        return (
            self.first,
            self.last,
            self.address,
            self.city,
            self.zipcd,
            self.phone,
            self.homeyr,
            self.home_size,
            self.estimated_value,
            self.home_sale_date,
        )

    def final_packager(self):
        return (
            self.first,
            self.last,
            self.address,
            self.city,
            self.zipcd,
            self.phone,
            self.homeyr,
            self.home_size,
            self.estimated_value,
            self.home_sale_date,
            self.mod_first,
            self.mod_last,
            self.mod_sqft,
            self.mod_yr,
            self.mod_pres,
            self.mod_url,
        )


# Main function that is called to determine the bar that should be set to
# maximize collection of housing square footage data
def square_call(square_bar=1980, all_info=tuple()):
    def square_limit(square_bar_test, all_info):
        num_square_ft = 0
        info_index = 0
        for client_line in all_info:
            if client_line.mod_passthrough == True:
                present_use = client_line.mod_pres.lower()
                if (
                    "condo" not in present_use
                    and "apartment" not in present_use
                    and "mobile home" not in present_use
                ):
                    if int(client_line.home_size) <= square_bar_test:
                        num_square_ft += 1

        return num_square_ft

    num_square_ft = square_limit(square_bar, all_info)
    if num_square_ft < 999:
        if square_limit(square_bar + 10, all_info) >= 999:
            return square_bar
        return square_call(square_bar + 10, all_info)
    else:
        if square_limit(square_bar - 10, all_info) < 999:
            return square_bar - 10
        return square_call(square_bar - 10, all_info)


# Function that threads use
def add_list(line):
    # Take address and converts to search friendly form
    # Converts spaces " " to "%20"
    client_line = Client(line).lower()
    address = client_line.address
    address = address.replace(" ", "%20")
    last_name = client_line.last
    def requester():
        try:
            # Takes pin_id or parcel number required to access web data and urls
            pin_id = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}"
            ).json()["items"][0]["PIN"]
            # Takes present_use data Ex:"Single Family(Res)" to put in csv file
            # Creates url based off of pin_id(Parcel Number)
            # Url is not verified to avoid web visit restriction
            url = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
            source = requests.get(
                f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
            ).json()

            taxpayer_name = source["items"][0]["TAXPAYERNAME"]
            present_use = source["items"][0]["PRESENTUSE"]
            # Parse more accurately
            if len(taxpayer_name) > 0:
                if str(last_name).lower() not in taxpayer_name.lower():
                    taxpayer_1 = taxpayer_name.replace("+", "|")
                    taxpayayer_2 = taxpayer_1.replace("&", "|")
                    name_list_1 = taxpayayer_2.split("|")
                    for name1 in name_list_1:
                        name1 = name1.strip()
                        name_list_2 = name1.split(" ")
                        if last_name.lower() == name_list_2[0].lower():
                            taxpayer_fname = ""
                            taxpayer_lname = ""
                            break
                        else:
                            if len(name_list_2) >= 2:
                                taxpayer_fname = name_list_2[1]
                                taxpayer_lname = name_list_2[0]
                else:
                    taxpayer_fname = ""
                    taxpayer_lname = ""
            else:
                taxpayer_fname = ""
                taxpayer_lname = ""
            # Signifies that process was successful to move onto access square footage data
            client.mod_passthrough = True
            client.mod_first = taxpayer_fname
            client_line.mod_first = taxpayer_fname
            client_line.mod_last = taxpayer_lname
            client_line.mod_pres = present_use
            client_line.mod_url = url
            client_line.mod_pin_id = pin_id
        except:
            client.mod_passthrough = False

    if client_line.mod_passthrough == False:
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
        # Loops through dictionary to see if dictionary result is in address
        for abbreviation, full in abb_dict.items():
            # Sees if results is in address and will fix search result and the computer well tell computer
            if f"%20{abbreviation}%20" in address:
                address = address.replace(abbreviation, full)
                client_line.mod_passthrough = True
        # If dictionary element changed, the program will submit another request for data to fix field
        if client_line.mod_passthrough:
            requester()
    return client_line


def square_footage(client_line):
    if client_line.mod_passthrough:
        # Takes square_ft data from clients
        pin_id = client_line.mod_pin_id
        present_use_lower = client_line.mod_pres.lower()
        if (
            "condo" not in present_use_lower
            and "apartment" not in present_use_lower
            and "mobile home" not in present_use_lower
        ):
            square_ft = int(client_line.home_size)
            if square_ft <= square_bar:
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
                    tr_sqft = table2.find_all("tr")[1]
                    tr_yr = table2.find_all("tr")[0]
                    try:
                        header_sqft = tr_sqft.find_all("td")[0].text.lower()
                        if header_sqft == "total square footage":
                            new_square_ft = tr_sqft.find_all("td")[1].text
                        else:
                            new_square_ft = "Error"
                        header_yr = tr_yr.find_all("td")[0].text.lower()
                        if header_yr == "year built":
                            new_year_built = tr_yr.find_all("td")[1].text
                        else:
                            new_year_built = "Error"
                    except:
                        new_square_ft = "Error"
                        new_year_built = "Error"
                        # Loops through tr tags in table
                        tr = table2.find_all("tr")
                        for value in tr:
                            try:
                                header_sqft = value.find_all("td")[0].text.lower()
                                # Sees if header is correct then will append
                                if header_sqft == "total square footage":
                                    new_square_ft = value.find_all("td")[1].text
                                    break
                            except:
                                pass
                        for value in tr:
                            try:
                                header_yr = value.find_all("td")[0].text.lower()
                                if header_yr == "year built":
                                    new_year_built = value.find_all("td")[1].text
                                    break
                            except:
                                pass
                except:
                    new_square_ft = "Error"
                    new_year_built = "Error"
            else:
                # Appends dashes to maintain csv structure
                new_square_ft = ""
                new_year_built = ""
        else:
            # Appends dashes to maintain csv structure
            new_square_ft = ""
            new_year_built = ""
        client_line.mod_sqft = new_square_ft
        client_line.mod_sqft = new_year_built
        return client_line.final_packager
    else:
        return client_line.final_packager


with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Maps function ensure the threads called first are executed first
        all_info = [client_line for client_line in executor.map(add_list, csv_reader)]
tuple(all_info)

# Calls function to get bar to set to
square_bar = square_call(square_bar=1980, all_info=all_info)

# Reminder to ensure program does not stop in execution
print("Reminder: Do not open the csv file that is being read or written!")

with open(new_PATH, "w") as new_file:
    csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
    # Adds additional elements to top row of csv data
    first_line.extend(
        (
            "Mod-Taxpayer First",
            "Mod-Taxpayer Last",
            "Mod-Real Square Footage",
            "Mod-Year Built",
            "Mod-Present Use",
            "Mod-URL",
        )
    )
    csv_writer.writerow(first_line)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Maps function ensure the threads called first are executed first
        for line in executor.map(square_footage, all_info):
            csv_writer.writerow(line)
print("Finished!")
