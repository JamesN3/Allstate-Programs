import csv
import openpyxl as pyxl

# Generate list of addresses in FIlter street names
wb = pyxl.load_workbook(
    "C:/Users/Public/Documents/Jamie's Work Folder/Filter street names.xlsx",
)
sheet = wb.worksheets[0]

row_count = sheet.max_row
column_count = sheet.max_column

compare_list = []

for row in range(1, row_count):
    for column in range(1, column_count):
        # Cell value is giving the location of in the csv
        cell = str(sheet.cell(row=row, column=column).value).lower()
        # Does not work as intended
        if cell != "none":
            # Does not work as intended
            if "*" in cell == False:
                compare_list.append(cell)
            else:
                # While statement does not work as intended
                while "*" in cell == True:
                    for i in range(0, 10):
                        copy_str = cell
                        copy_str.replace("*", str(i))
                        compare_list.append(copy_str)

print(compare_list)

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