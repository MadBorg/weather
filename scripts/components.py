import requests
import json

url = "https://api.nilu.no/"

def components():
    url_args = "lookup/components"
    r = requests.get(url + url_args)
    if not r.ok:
        raise Exception("r not ok")

    data = r.json()
    with open("weather\\static\\components.json", "w+") as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    components()