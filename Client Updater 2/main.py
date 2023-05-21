# Author: James Ngai (Allstate "HALE INSURANCE, INC.")
# Program built solely for the use of Allstate Hale Insurance Inc
#
# Program takes prexisting client data and adds the client's
# Housing Square Footage(if num_square_ft<1000), Present Use, and property detail url
#
# Data collection source
# https://gismaps.kingcounty.gov/parcelviewer2/

import requests
import csv
import concurrent.futures
from os import path
from bs4 import BeautifulSoup
from json import load
from filter import *
from sqft_optimizer import *
from fetch import *
from taxpayer_name_parser import *

def main():
    # Message is to inform user about program operations
    print(
        "\nOutput file will be in same folder as input file\nNew file name will be "
        "new_{file_name}.csv"
        ""
    )

    # Takes the PATH of the csv file and stores info in constant PATH
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

    class Client:
        # Initalizes all variables for object storing prospective client's data
        def __init__(self, line):
            self.__first = line[0]
            self.__last = line[1]
            self.__address = line[2]
            self.__city = line[3]
            self.__state = line[4]
            self.__zipcd = line[5]
            self.__phone = line[6]
            self.__mailstat = line[8]
            self.__callstat = line[9]
            self.__phonestat = line[10]
            self.__custstat = line[11]
            self.__homeyr = line[12]
            self.__home_size = int(line[13])
            self.__estimated_value = line[14]
            self.__home_sale_date = line[15]

            # Mod suffix indicates these data types are appended by new API data collected by program

            # Variable is a booean which indicates the amount of success in the data collection process
            self.mod_passthrough = False 

            # Data collected first/last name
            self.mod_first = "" 
            self.mod_last = ""
            self.mod_full = ""

            # Data collected year of construction for insurance property
            self.mod_yr = ""

            # Data collected square footage of property
            self.mod_sqft = ""

            # Indicates the present use of the property (e.g: Single Family Residence, Medical Use...)
            self.mod_pres = ""
            self.mod_url = "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"

            # Data point containing access code to gather data from King County Parcel Viewer API
            self.mod_pin_id = ""

        def final_packager(self):
            return (
                self.__first,
                self.__last,
                self.__address,
                self.__city,
                self.__state,
                self.__zipcd,
                self.__phone,
                "",
                self.__mailstat,
                self.__callstat,
                self.__phonestat,
                self.__custstat,
                self.__homeyr,
                self.__home_size,
                self.__estimated_value,
                self.__home_sale_date,
                self.mod_first,
                self.mod_last,
                self.mod_full,
                self.mod_yr,
                self.mod_sqft,
                self.mod_pres,
                self.mod_url,
            )

    # Function that threads use
    def threader(line):
        # Take address and converts to search friendly form
        # Converts spaces " " to "%20"
        client = Client(line)
        address = client._Client__address.lower()
        address = address.replace(" ", "%20")
        try:
            taxpayer_name, present_use, url, pin_id = fetch(address)
        except:
            new_address = abb_list(address)
            if new_address != address:
                try: 
                    taxpayer_name, present_use, url, pin_id = fetch(new_address)
                except:
                    pass
                else:
                    client.mod_pres = present_use
                    client.mod_full = taxpayer_name
                    client.mod_url = url
                    client.mod_pin_id = pin_id
                    tax_parse(client)
        else:
            client.mod_pres = present_use
            client.mod_full = taxpayer_name
            client.mod_url = url
            client.mod_pin_id = pin_id
            tax_parse(client)
        finally:
            return client


    def square_footage(client):
        if not client.mod_passthrough:
            return client
        # Takes square_ft data from clients
        pin_id = client.mod_pin_id
        present_use_lower = client.mod_pres.lower()
        new_square_ft = ""
        new_year_built = ""
        if not present_use_filter(present_use_lower):
            return client
        square_ft = client._Client__home_size
        if square_ft > square_bar:
            return client
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
        client.mod_sqft = new_square_ft
        client.mod_yr = new_year_built
        return client
            


    with open(PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        first_line = next(csv_reader)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Maps function ensure the threads called first are executed first
            clients = [client_line for client_line in executor.map(threader, csv_reader)]

    # Calls function to get bar to set to
    square_bar = square_call(2000, clients)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Maps function ensure the threads called first are executed first
        clients = [client for client in executor.map(square_footage, clients)]
        
    # Reminder to ensure program does not stop in execution
    print("Reminder: Do not open the csv file that is being read or written!")

    with open(new_PATH, "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        # Adds additional elements to top row of csv data
        first_line.extend(
            (
                "Mod-Taxpayer First",
                "Mod-Taxpayer Last",
                "Mod-Full",
                "Mod-Year Built",
                "Mod-Real Square Footage",
                "Mod-Present Use",
                "Mod-URL",
            )
        )
        csv_writer.writerow(first_line)
        for client in clients:
            csv_writer.writerow(client.final_packager())
    
    print("Finished!")

if __name__ == "__main__":
    main()