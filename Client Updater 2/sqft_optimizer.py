from filter import present_use_filter

# square_call function is called to determine the square footage maximum bar that should be set for data collection
# As of September 2021 max collection is 1000 data points
# Implementation uses recursive optimizer to cycle for max collection square footage
def square_call(square_bar, clients):
    print("sqft optimizing")
    def square_limit(square_bar_test):
        num_square_ft = 0
        for client_line in clients:
            if not client_line.mod_passthrough:
                continue
            present_use_lower = client_line.mod_pres.lower()
            if not present_use_filter(present_use_lower):
                continue
            if client_line._Client__home_size <= square_bar_test:
                num_square_ft += 1
        return num_square_ft

    num_square_ft = square_limit(square_bar)
    if num_square_ft <= 1000:
        while (num_square_ft <= 1000):
            square_bar += 10
            num_square_ft = square_limit(square_bar)
        return square_bar-10
    if num_square_ft > 1000:
        while (num_square_ft > 1000):
            square_bar -= 10
            num_square_ft = square_limit(square_bar)
        return square_bar