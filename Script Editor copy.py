import csv


def compare(x, y):
    if x[x.index(" ") :] == y[y.index(" ") :]:
        x_max = int(x.replace("*", "9")[: x.index(" ")])
        x_min = int(x.replace("*", "0")[: x.index(" ")])
        y_num = int(y[: y.index(" ")])
        if y_num >= x_min and y_num <= x_max:
            return True
    return False


# Opens file that is being filtered
# Contains all customer data
print("All files must be csv")
file_original = input(
    "Please input csv file name for customer csv list. Omit csv endtag\n"
)
filter_list = input("Please input csv file name with filter list. Omit csv endtag\n")

with open(f"C:/Users/jamie/Downloads/{file_original}.csv", "r") as original_file:

    csv_reader = csv.reader(original_file)
    done_first_line = True
    first_line = next(csv_reader)

    # Writes to new csv file with filter value rows omitted
    # Reconstructs orginal file, omitting filtered
    with open(f"C:/Users/jamie/Downloads/new_{file_original}.csv", "w") as new_file:

        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")

        # Writes to new file with the rows that are omitted
        with open(
            f"C:/Users/jamie/Downloads/omit_new_{file_original}.csv", "w"
        ) as new_file_omit:
            csv_writer_omit = csv.writer(
                new_file_omit, delimiter=",", lineterminator="\n"
            )
            for line in csv_reader:

                # Take csv file that is being compared
                with open(
                    f"C:/Users/jamie/Downloads/{filter_list}.csv", "r"
                ) as csv_filter:
                    if done_first_line:
                        csv_writer.writerow(first_line)
                        csv_writer_omit.writerow(first_line)
                        done_first_line = False
                    csv_checker = csv.reader(csv_filter)
                    check = True
                    for line_checker in csv_checker:
                        element = str(line_checker[0]).lower()
                        if "*" not in element and element in line[2].lower():
                            check = False
                            csv_writer_omit.writerow(line)
                            break
                        elif "*" in element:
                            if compare(element, line[2].lower()):
                                check = False
                                csv_writer_omit.writerow(line)
                                break
                if check == True:
                    csv_writer.writerow(line)