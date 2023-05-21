from filter import present_use_filter, tax_check_name

def tax_parse(client):
    last_name = client._Client__last
    taxpayer_list_name = ["",""]
    if len(taxpayer_name) > 0 and str(last_name).lower() not in taxpayer_name.lower():
        parsers = ("+", "and", "AND", "And")
        for element in parsers:
            taxpayer_name = taxpayer_name.replace(element, "&")
        name_list_1 = taxpayer_name.split("&")
        for name1 in name_list_1:
            name1 = name1.strip()
            name_list_2 = name1.split(" ")
            if tax_check_name(name_list_2) == False or last_name.lower() == name_list_2[0].lower():
                taxpayer_list_name[0] = ""
                taxpayer_list_name[1] = ""
                break
            else:
                if len(name_list_2) >= 2:
                    taxpayer_list_name[0] = name_list_2[1].title()
                    taxpayer_list_name[1] = name_list_2[0].title()
        # Signifies that process was successful to move onto access square footage data
        client.mod_passthrough = True
        client.mod_first = taxpayer_list_name[0]
        client.mod_last = taxpayer_list_name[1]