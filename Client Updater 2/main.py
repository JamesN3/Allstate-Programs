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
from filter import *
from sqft_optimizer import *
from fetch import *
from taxpayer_name_parser import *
from Client import Client

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

    # Function that threads use
    def threader1(line):
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
                    client.mod_passthrough = True
                    tax_parse(client)
        else:
            client.mod_pres = present_use
            client.mod_full = taxpayer_name
            client.mod_url = url
            client.mod_pin_id = pin_id
            client.mod_passthrough = True
            tax_parse(client)
        finally:
            return client


    def threader2_sqft(client):
        if not square_footage_filter(client, square_bar):
            return client
        # Takes square_ft data from clients
        pin_id = client.mod_pin_id
        present_use_lower = client.mod_pres.lower()
        new_square_ft = ""
        new_year_built = ""
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
            clients = [client_line for client_line in executor.map(threader1, csv_reader)]

    # Calls function to get bar to set to
    square_bar = square_call(2000, clients)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Scrapping Square Footage\n")
        # Maps function ensure the threads called first are executed first
        clients = [client for client in executor.map(threader2_sqft, clients)]
        
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