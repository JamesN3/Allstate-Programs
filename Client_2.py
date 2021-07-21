import csv
import requests
import pandas as pd
from os import path

PATH = str(
    input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
)

while not path.exists(PATH):
    print("Error with file path, check it is correct and compare with example")
    PATH = str(
        input("Insert file path\nEx: C:\\Users\\Allstate\\Downloads\\August2021.csv\n")
    )


def add_list(line):
    address = line[2]
    print(address)
    address = address.replace(" ", "%20")
    try:
        requests.get("dadadada")
    except:
        address = address.lower()
        passthrough = False
        abb_dict = {
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
        print(passthrough)


with open(PATH, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    first_line = next(csv_reader)
    for line in csv_reader:
        add_list(line)
print("Finished!")