# Author: James Ngai(Allstate "HALE INSURANCE, INC.")
# Program built solely for the use of Allstate Hale Insurance Inc
#
# Program takes prexisting client data aand compiles it into a csv file

import requests
import csv
import concurrent.futures
import threading
import queue
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import Frame
from tkinter import messagebox


class Application:
    file_path = ""
    my_progress = None

    def __init__(self):
        def get_dir():
            Application.file_path = filedialog.askopenfilename(
                title="Select A File",
                filetypes=(("csv files", "*.csv"),),
            )

        def submit_button():
            continuer = True
            self.button.destroy()
            self.Button_2.destroy()

        root.title("Yumio Marketer")
        root.iconbitmap("Yumio logo.ico")
        root.geometry("600x400")
        self.button = Button(
            root, text="Select File", pady=20, command=get_dir()
        ).pack()
        self.my_label = Label(root, text=self.file_path).pack()
        self.my_progress = ttk.Progressbar(
            root, orient=HORIZONTAL, length=300, mode="determinate"
        ).pack(pady=20)
        self.Button_2 = Button(root, text="Submit", command=submit_button)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def step(self):
        self.my_progress.start(incrementor)
        root.update()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            root.destroy()
            quit()

    def finish(self):
        self.my_label_3 = Label(root, text="Finished").pack()

    def reminder(self):
        self.my_label_2 = Label(
            root, text="Do not open csv file being written or read"
        ).pack()


# Main function that is called to determine the bar that should be set to
# maximize collection of housing square footage data
def square_call(square_bar=1980, all_info=tuple()):
    def square_limit(square_bar_test, all_info):
        with open(PATH, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            num_square_ft = 0
            info_index = 0
            for line, info in zip(csv_reader, all_info):
                if info[0] == True:
                    present_use = info[2].lower()
                    if (
                        "condo" not in present_use
                        and "apartment" not in present_use
                        and "mobile home" not in present_use
                    ):
                        if int(line[8]) <= square_bar_test:
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
    address = str(line[2])
    address = address.replace(" ", "%20")

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
                if str(line[1]).lower() not in taxpayer_name.lower():
                    taxpayer_1 = taxpayer_name.replace("+", "|")
                    taxpayayer_2 = taxpayer_1.replace("&", "|")
                    name_list_1 = taxpayayer_2.split("|")
                    for name1 in name_list_1:
                        name1 = name1.strip()
                        name_list_2 = name1.split(" ")
                        if line[1].lower() == name_list_2[0].lower():
                            taxpayer_name = ""
                            break
                else:
                    taxpayer_name = ""
            else:
                taxpayer_name = ""
            # Signifies that process was successful to move onto access square footage data
            return (True, taxpayer_name, present_use, url, pin_id)
        except:
            return (False,)

    all_info = requester()
    if all_info[0] == False:
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
            all_info = requester()
    return all_info


def square_footage(all_info, line):
    if all_info[0] == True:
        # Takes square_ft data from clients
        taxpayer_name = all_info[1]
        present_use = all_info[2]
        url = all_info[3]
        pin_id = all_info[4]
        present_use_lower = all_info[2].lower()
        if (
            "condo" not in present_use_lower
            and "apartment" not in present_use_lower
            and "mobile home" not in present_use_lower
        ):
            square_ft = int(line[8])
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
        line.extend(
            (
                taxpayer_name,
                new_square_ft,
                new_year_built,
                present_use,
                url,
            )
        )
        return line
    else:
        line.extend(("", "", "", "", error_message))
        return line


root = Tk()

file_opener = Application()

PATH = file_opener.file_path


with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    row_count = sum(1 for row in csv_reader)
    incrementor = 100 / row_count


# Creates new file path for csv file that is being written
last_index = PATH.rfind("\\")
new_PATH = f"{PATH[0 : last_index + 1]}new_{PATH[last_index + 1 :]}"

with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Maps function ensure the threads called first are executed first
        all_info = [line for line in executor.map(add_list, csv_reader)]
tuple(all_info)

# Calls function to get bar to set to
square_bar = square_call(square_bar=1980, all_info=all_info)

# Reminder to ensure program does not stop in execution
file_opener.reminder()
# The message that is sent when an error occurs
error_message = "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"

with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    with open(new_PATH, "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        # Adds additional elements to top row of csv data
        first_line.extend(
            (
                "Mod-Taxpayer Name",
                "Mod-Real Square Footage",
                "Mod-Year Built",
                "Mod-Present Use",
                "Mod-URL",
            )
        )
        csv_writer.writerow(first_line)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Maps function ensure the threads called first are executed first
            for line in executor.map(square_footage, all_info, csv_reader):
                csv_writer.writerow(line)
                file_opener.step()
file_opener.finish()
root.mainloop()