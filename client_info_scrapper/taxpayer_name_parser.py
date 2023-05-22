from filter import present_use_filter, tax_check_name

# def tax_parse(client):
#     last_name = client._Client__last
#     taxpayer_name = client.mod_full
#     taxpayer_list_name = ["",""]
#     if len(taxpayer_name) > 0 and str(last_name).lower() not in taxpayer_name.lower():
#         parsers = ("+", "and", "AND", "And")
#         for element in parsers:
#             taxpayer_name = taxpayer_name.replace(element, "&")
#         name_list_1 = taxpayer_name.split("&")
#         for name1 in name_list_1:
#             name1 = name1.strip()
#             name_list_2 = name1.split(" ")
#             if tax_check_name(name_list_2) == False or last_name.lower() == name_list_2[0].lower():
#                 taxpayer_list_name[0] = ""
#                 taxpayer_list_name[1] = ""
#                 break
#             else:
#                 if len(name_list_2) >= 2:
#                     taxpayer_list_name[0] = name_list_2[1].title()
#                     taxpayer_list_name[1] = name_list_2[0].title()
#         # Signifies that process was successful to move onto access square footage data
#     client.mod_first = taxpayer_list_name[0]
#     client.mod_last = taxpayer_list_name[1]


def tax_parse(client):
    last_name = client._Client__last.lower()
    taxpayer_name = client.mod_full
    taxpayer_name_lower = taxpayer_name.lower()
    if len(taxpayer_name) == 0 or last_name in taxpayer_name_lower or not tax_check_name(taxpayer_name):
        return client
    parsers = ("+", " and ", " AND ", " And ", "_")
    for element in parsers:
        taxpayer_name = taxpayer_name.replace(element, "&")
    
    taxpayer_list = taxpayer_name.split("&")
    
    match len(taxpayer_list):
        case 1:
            name_list = taxpayer_list[0].split(" ")
            match len(name_list):
                case 1:
                    client.mod_last = name_list[0].strip().title()
                case 2:
                    client.mod_first = name_list[1].strip().title()
                    client.mod_last = name_list[0].strip().title()
                case _:
                    client.mod_first = name_list[1].strip().title()
                    client.mod_last = name_list[0].strip().title()
        case _:
            def counter(name_list):
                num_not_ones = 0
                for name in name_list:
                    if len(name) != 1:
                        num_not_ones += 1
                return num_not_ones
            taxpayer_list[0] = taxpayer_list[0].strip()
            taxpayer_list[1] = taxpayer_list[1].strip()
            name_list1 = taxpayer_list[0].split(" ")
            name_list2 = taxpayer_list[1].split(" ")
            num_not_ones_1 = counter(name_list1)
            num_not_ones_2 = counter(name_list2)
            match(num_not_ones_1, num_not_ones_2):
                case (1,1):
                    client.mod_last = name_list1[0].title()
                case(_,1):
                    client.mod_first = name_list1[1].title()
                    client.mod_last = name_list1[0].title()
                case(1,_):
                    client.mod_first = name_list2[1].title()
                    client.mod_last = name_list2[0].title()
    return client