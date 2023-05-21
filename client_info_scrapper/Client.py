class Client:
    # Initalizes all variables for object storing prospective client's data
    def __init__(self, line):
        self.__first = line[0]
        self.__last = line[1]
        self.__address = line[2]
        self.__city = line[3]
        self.__state = line[4]
        self.__zipcd = line[5]
        self.__phone = line[6]
        self.__mailstat = line[8]
        self.__callstat = line[9]
        self.__phonestat = line[10]
        self.__custstat = line[11]
        self.__homeyr = line[12]
        self.__home_size = int(line[13])
        self.__estimated_value = line[14]
        self.__home_sale_date = line[15]

        # Mod suffix indicates these data types are appended by new API data collected by program

        # Variable is a booean which indicates the amount of success in the data collection process
        self.mod_passthrough = False 

        # Data collected first/last name
        self.mod_first = "" 
        self.mod_last = ""
        self.mod_full = ""

        # Data collected year of construction for insurance property
        self.mod_yr = ""

        # Data collected square footage of property
        self.mod_sqft = ""

        # Indicates the present use of the property (e.g: Single Family Residence, Medical Use...)
        self.mod_pres = ""
        self.mod_url = "Error — Refer to https://blue.kingcounty.com/assessor/erealproperty/ErrorDefault.htm?aspxerrorpath=/Assessor/eRealProperty/Detail.aspx"

        # Data point containing access code to gather data from King County Parcel Viewer API
        self.mod_pin_id = ""

    def final_packager(self):
        return (
            self.__first,
            self.__last,
            self.__address,
            self.__city,
            self.__state,
            self.__zipcd,
            self.__phone,
            "",
            self.__mailstat,
            self.__callstat,
            self.__phonestat,
            self.__custstat,
            self.__homeyr,
            self.__home_size,
            self.__estimated_value,
            self.__home_sale_date,
            self.mod_first,
            self.mod_last,
            self.mod_full,
            self.mod_yr,
            self.mod_sqft,
            self.mod_pres,
            self.mod_url,
        )