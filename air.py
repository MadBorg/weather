import requests
import pandas as pd
import datetime
import IPython as IP
import psycopg2 as psql
import re
from pprint import pprint


class air:
    url = "https://api.nilu.no/"



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

    def _establish_connection(self):
        user = "db_air"
        pwd = "password"
        db = "weather"
        port = "5432"
        host = "localhost"
        connection = \
            f"dbname='" + db + "' " + \
            f"user='{user}' " + \
            f"port='{port}' " + \
            f"host='{host}' " + \
            f"password='{pwd}' "

        conn = psql.connect(connection)

        # self.conn = conn
        return conn

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

    def get_stations(self):
        r = requests.get(self.url + "lookup/stations")
        stations = r.json()
        
        self.stations = stations
        return stations
   # pandas refactoring
    
   # database
    @property
    def conn(self):
        return self._establish_connection()

    def obs_to_db(self):
        pass

    def obs_utd_to_db(self):
        """
            Gathering the up to date data, using osb_to_db.
        """
        pass

    def update_stations_db(self):
        stations = self.get_stations()

        q = "INSERT INTO Station(id, eoi, name, latitude, longitude, zone, municipality, area, description, components, status) VALUES \n"
        
        for station in stations: # O(n)
            if not (station["id"] is None or station["eoi"] is None):
                q += f"({station['id']}, "  + \
                    f"'{station['eoi']}', " + \
                    f"'{station['station']}', " + \
                    f"{station['latitude']}, " + \
                    f"{station['longitude']}, " + \
                    f"'{station['zone']}', " + \
                    f"'{station['municipality']}', " + \
                    f"'{station['area']}', " + \
                    f"'{station['description']}', " + \
                    f"'{station['components']}', " + \
                    f"'{station['status']}'), \n" 
        q = re.sub(", \n$", ";", q) # substituding then end lokking like <, > folowing the regexp ", $" with a ;  
        with open("q.txt", "w+") as file:
            file.write(q)

        conn = self.conn
        cur = conn.cursor()
        cur.execute(q)
        self.conn.commit()

   # show data

    def matrix_plot(self):
        pass


if __name__ == "__main__":
    tmp = air()
    data = tmp.get_aq()
    # data = tmp.get_aq(utd=False, fromtime="2019-01-01", totime="2019-01-03", station="alnabru")
    tmp.update_stations_db()
    IP.embed()
