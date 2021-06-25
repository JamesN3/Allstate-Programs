from bs4 import BeautifulSoup
import requests
import csv

source = requests.get("https://gismaps.kingcounty.gov/parcelviewer2/").text

soup = BeautifulSoup(source, "lxml")

something = soup.find("div", class_="dijitReset dijitInputField dijitInputContainer")
print(something)
something1 = something.find("input", class_="dijitReset dijitInputInner")

print(something1)


file_name = str(input("What is your file name with addresses?"))
with open(f"C:/Users/jamie/Downloads/{file_name}.csv") as csv_original:
    with open(f"C:/Users/jamie/Downloads/new_residency_{file_name}.csv") as new_csv:
        pass