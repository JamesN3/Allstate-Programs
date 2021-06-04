import csv
import pandas as pd
from openpyxl import load_workbook

# Generate list of addresses in FIlter street names
wb = load_workbook(
    "C:/Users/Public/Documents/Jamie's Work Folder.xlsx", use_iterators=True
)
sheet = wb.worksheets[0]

row_count = sheet.max_row
column_count = sheet.max_column

compare_list = []

with open(
    "C:/Users/Public/Documents/Jamie's Work Folder/July2021.csv", "r"
) as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader)

    with open(
        "C:/Users/Public/Documents/Jamie's Work Folder/new_July2021.csv", "w"
    ) as new_file:
        csv_writer = csv.writer(new_file, delimiter=",")
        for line in csv_reader:
            for compare_value in compare_list:
                if compare_value.lower() != line[2].lower():
                    csv_writer.writerow(line)