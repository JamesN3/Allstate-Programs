# The following set contains present uses which are considered uninsurable
ban_present_use = {"condo", "apartment", "townhouse", "medical", "dental", "industrial", "corportation", "estates"}
ban_tax_name = {"city", "inc", "ltd", "trust", "irrevocable", "revocable", "llc", "living", "property", "family", "farm", "bank", "home", "relocation", "relocatio","holdings", "investment", "mortgage", "mutual", "development", "enterprises", "project", "work", "industrial", "county-parks", "national", "transfer", "toll", "ttee"}
abb_dict = {
            "mt": "mountain",
            "mount": "mt",
            "woodinvl": "woodinville",
            "sunbreak": "sun break",
            "shr": "shore",
            "cntry": "country",
            "clb": "club",
            "lk": "lake",
            "shangrila": "shangri la",
            "shoreclub": "shore club",
        }

def tax_check_name(tax_name):
    for name in tax_name:
        if name.lower() in ban_tax_name:
            return False  
    return True

# Uses set comparison to determine if the present use of the building is a possible prospetive client
def present_use_filter(present_use_lower):
    for ban_item in ban_present_use:
        if ban_item in present_use_lower:
            return False
    return True

def abb_list(address):
    # Loops through dictionary to see if dictionary result is in address
    for abbreviation, full in abb_dict.items():
        # Sees if results is in address and will fix search result and the computer well tell computer
        if f"%20{abbreviation}%20" in address:
            address = address.replace(abbreviation, full)
    
    return address

def square_footage_filter(client, square_bar):
    # Takes square_ft data from clients
    pin_id = client.mod_pin_id
    present_use_lower = client.mod_pres.lower()
    new_square_ft = ""
    new_year_built = ""
    square_ft = client._Client__home_size
    if square_ft > square_bar or (not client.mod_passthrough) or (not present_use_filter(present_use_lower)):
        return False
    return True