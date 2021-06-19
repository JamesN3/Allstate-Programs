import csv


def compare(x, y):
    if x[x.index(" ") :] == y[y.index(" ") :]:
        x_max = int(x.replace("*", "9")[: x.index(" ")])
        x_min = int(x.replace("*", "0")[: x.index(" ")])
        y_num = int(y[: y.index(" ")])
        if y_num >= x_min and y_num <= x_max:
            return True
    return False


with open("C:/Users/jamie/Downloads/August2021.csv", "r") as original_file:

    csv_reader = csv.reader(original_file)
    next(csv_reader)
    # Writes to new csv file with values omitted
    with open("C:/Users/jamie/Downloads/new_August2021.csv", "w") as new_file:
        csv_writer = csv.writer(new_file, delimiter=",", lineterminator="\n")
        # Writes to new file previous csv file but first checks if value should be added to csv
        with open(
            "C:/Users/jamie/Downloads/omit_new_August2021.csv", "w"
        ) as new_file_omit:
            csv_writer_omit = csv.writer(
                new_file_omit, delimiter=",", lineterminator="\n"
            )
            for line in csv_reader:
                with open("C:/Users/jamie/Downloads/Filter List.csv") as csv_filter:
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