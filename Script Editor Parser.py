import csv
import openpyxl as pyxl

wb = pyxl.load_workbook(
    "C:/Users/Public/Documents/Jamie's Work Folder/Filter street names.xlsx",
)
sheet = wb.worksheets[0]

row_count = sheet.max_row
column_count = sheet.max_column