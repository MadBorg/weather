import requests
import pandas as pd
import datetime
import IPython as IP
import psycopg2 as psql


class air:
    url = "https://api.nilu.no//"

    def __init__(self):
        print(self.url)
  # private
   # get
    def _get_data(self, url, params, utd, fromtime, totime, latitude, longitude, radius , station):
       # asserts
        if radius:
            assert radius  <= 20 and radius > 0,  "Radius can at max be 20 km and at at least be more then 0, given radius is:" + radius

        if not utd: #historical
            # assert type(totime) is datetime.date or type(totime) is datetime.datetime
            # assert type(fromtime) is datetime.date or type(fromtime) is datetime.datetime

            if radius and longitude and latitude:
                pass
            if station:
                pass
            else:
                raise ValueError("If utd is false fromtime and totime must be specified, along with ether station or longitude, latitude and radius")

            if fromtime and totime:
                # TODO: add posibility for time aswell
                if type(totime) is str:
                    totime = datetime.datetime.strptime(totime, "%Y-%m-%d")
                if type(fromtime) is str:
                     fromtime = datetime.datetime.strptime(fromtime, "%Y-%m-%d")
                # IP.embed()
                assert (totime - fromtime).days <= 30, "Date span must be under 30 days"
       # komponents
        if utd:
            url += "utd/"
        else:
            url += f"historical/{fromtime}/{totime}/"

        if latitude and longitude and radius:
            url += f"{latitude}/{longitude}/{radius}/"
        elif station:
            url += f"{station}/"
       # --
        r = requests.get(url, params=params)
        data = r.json()
        return data

  # public
   # Get
    def get_aq(self, params=None, utd=True, fromtime=None, totime=None, latitude=None, longitude=None, radius =None, station=None):
        url = self.url + "aq/"
        data = self._get_data(url, params, utd, fromtime, totime, latitude, longitude, radius, station)
        return data

    def get_obs(self, params=None, utd=True, fromtime=None, totime=None, latitude=None, longitude=None, radius =None, station=None):
        url = self.url + "obs/"
        data = self._get_data(url, params, utd, fromtime, totime, latitude, longitude, radius, station)
        return data

    def get_stats(self, params):
        url = self.url + "stats/"
        r = requests.get(url, params=params)
        data = r.json()
        return data

    def get_lookup(self, params):
        url = self.url + "lookup/"
        r = requests.get(url, params=params)
        data = r.json()
        return data

   # pandas refactoring
    
   # database
   # show data

    def matrix_plot(self):
        pass


if __name__ == "__main__":
    tmp = air()
    data = tmp.get_aq()
    # data = tmp.get_aq(utd=False, fromtime="2019-01-01", totime="2019-01-03", station="alnabru")
    IP.embed()
