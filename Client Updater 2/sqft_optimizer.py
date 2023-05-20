from filter import present_use_filter

# square_call function is called to determine the square footage maximum bar that should be set for data collection
# As of September 2021 max collection is 1000 data points
# Implementation uses recursive optimizer to cycle for max collection square footage
def square_call(square_bar=2000, all_info=tuple()):
    def square_limit(square_bar_test, all_info):
        num_square_ft = 0
        for client_line in all_info:
            if client_line.mod_passthrough == True:
                present_use_lower = client_line.mod_pres.lower()
                if (
                    present_use_filter(present_use_lower)
                ):
                    if client_line._Client__home_size <= square_bar_test:
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