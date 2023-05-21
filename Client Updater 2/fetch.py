import requests

def fetch(address):
    try:
        pin_id = requests.get(f"https://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add={address}").json()["items"][0]["PIN"]
        # Takes present_use data Ex:"Single Family(Res)" to put in csv file
        # Creates url based off of pin_id(Parcel Number)
        # Url is not verified to avoid web visit restriction
        url = f"https://blue.kingcounty.com/Assessor/eRealProperty/Detail.aspx?ParcelNbr={pin_id}"
        source = requests.get(
            f"https://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin={pin_id}"
        ).json()

        taxpayer_name = source["items"][0]["TAXPAYERNAME"]
        present_use = source["items"][0]["PRESENTUSE"]
        return taxpayer_name, present_use, url, pin_id
    except RuntimeError:
        print("Runtime Error in fetch.py\n")
        raise
    except KeyError:
        print("Key Error in fetch.py\n")
        raise
    except requests.HTTPError:
        print("HTTP Error in fetch.py\n")
        raise
    except requests.ConnectionError:
        print("Connection Error in fetch.py\n")
        raise
    except requests.Timeout:
        print("Timeout Error in fetch.py\n")
        raise
    except requests.InvalidURL:
        print("Invalid URL in fetch.py\n")
        raise
    except requests.InvalidProxyURL:
        print("Invalid ProxyURL in fetch.py\n")
        raise
    except:
        print("Unknown Error in fetch.py\n")
        raise
