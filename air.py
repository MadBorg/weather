import requests
import pandas as pd
import datetime
import IPython as IP
import psycopg2 as psql
import re
import datetime
from pprint import pprint


class air:
    url = "https://api.nilu.no/"



    def __init__(self):
        print(self.url)
        
  # private
    def _establish_connection(self):
        user = "worker"
        pwd = "sander"
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

   # get
    def _get_data(self, url, params, utd, fromTime, toTime, latitude, longitude, radius , station):
       # asserts
        if radius:
            assert radius  <= 20 and radius > 0,  "Radius can at max be 20 km and at at least be more then 0, given radius is:" + radius

        if not utd: #historical
            # assert type(toTime) is datetime.date or type(toTime) is datetime.datetime
            # assert type(fromTime) is datetime.date or type(fromTime) is datetime.datetime

            if radius and longitude and latitude:
                pass
            if station:
                pass
            else:
                raise ValueError("If utd is false fromTime and toTime must be specified, along with ether station or longitude, latitude and radius")

            if fromTime and toTime:
                # TODO: add posibility for time aswell
                if type(toTime) is str:
                    toTime = datetime.datetime.strptime(toTime, "%Y-%m-%d")
                if type(fromTime) is str:
                     fromTime = datetime.datetime.strptime(fromTime, "%Y-%m-%d")
                # IP.embed()
                assert (toTime - fromTime).days <= 30, "Date span must be under 30 days"
       # komponents
        if utd:
            url += "utd/"
        else:
            url += f"historical/{fromTime}/{toTime}/"

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
    def get_aq(self, params=None, utd=True, fromTime=None, toTime=None, latitude=None, longitude=None, radius =None, station=None):
        url = self.url + "aq/"
        data = self._get_data(url, params, utd, fromTime, toTime, latitude, longitude, radius, station)
        return data

    def get_obs(self, params=None, utd=True, fromTime=None, toTime=None, latitude=None, longitude=None, radius =None, station=None):
        url = self.url + "obs/"
        data = self._get_data(url, params, utd, fromTime, toTime, latitude, longitude, radius, station)
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
    
    def get_obs_historical(self, fromTime, toTime, station=None,  latitude=None, longitude=None, radius=None):
        # TODO: implement for station and area
        print(f"     Getting data: {fromTime}, {toTime}")
        conn = self.conn
        cur = conn.cursor()

        url = self.url + "/obs/historical/" + f"{fromTime}/{toTime}"
        if station:
            url += f"/{station}"
        elif latitude and longitude and radius:
            url += f"{latitude}/{longitude}/{radius}"
        else:
            raise ValueError("location or station must be given! (get_obs_historical)")
        r = requests.get(url)
        data = r.json()
        print(f"     Done with data!")
        return data

    def get_obs_utd(self):
        return self.get_obs()

    def get_components(self):
        r = requests.get(self.url + "lookup/components/")
        data = r.json()
        return data

   # pandas refactoring
    
   # database
    @property
    def conn(self):
        return self._establish_connection()

    @property
    def stations(self):
        q = "SELECT name FROM Station;"
        conn = self.conn
        cur = conn.cursor()
        cur.execute(q)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def obs_to_db(self):
        pass

    def insert_obs_utd_to_db(self):
        """
            Gathering the up to date data, using osb_to_db.
        """


    def update_stations(self):
        stations = self.get_stations()
        conn = self.conn
        cur = conn.cursor()

        q = """INSERT INTO Station (id, eoi, name, latitude, longitude, zone, municipality, area, description, components, status)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
            """

        for station in stations: # O(n)
            if not (station["id"] is None or station["eoi"] is None):
                data = (
                    station['id'],
                    station['eoi'],
                    station['station'],
                    station['latitude'],
                    station['longitude'],
                    station['zone'],
                    station['municipality'],
                    station['area'],
                    station['description'],
                    station['components'],
                    station['status'],
                )
                
                cur.execute(q, data)
        conn.commit()
        cur.close()
        conn.close()

    def update_components(self):
        components = self.get_components()
        conn = self.conn
        cur = conn.cursor()
        q = """
            INSERT INTO Component (id, component)
            VALUES
                (DEFAULT, %s) ON CONFLICT DO NOTHING;
            """
        for component in components:
            data = (
                component["component"],
                )
            # print(f"data: {data}, type(data): {type(data)}")
            cur.execute(q, data)
        conn.commit()
        cur.close()

    def update_obs_utd(self):
        obses = self.get_obs_utd()
        conn = self.conn
        cur = conn.cursor()
        q = """
            INSERT INTO Reading (eoi, time_from, time_to, value, id_component)
            SELECT %s, %s, %s, %s, c.id
            FROM component AS c
            WHERE c.component = %s
            ON CONFLICT DO NOTHING;
            """
        for obs in obses:
            if not obs['eoi'] is None:
                data = (
                    obs['eoi'],
                    obs['fromTime'],
                    obs['toTime'],
                    obs['value'],
                    obs['component'],
                )
                cur.execute(q, data)
        conn.commit()
        cur.close()

    def update_obs_historical(self, fromTime, toTime, station="all"):
        obses = self.get_obs_historical(fromTime, toTime, station)
        conn = self.conn
        cur = conn.cursor()
        q = """
            INSERT INTO Reading (eoi, time_from, time_to, value, id_component)
            SELECT %s, %s, %s, %s, c.id
            FROM component AS c
            WHERE c.component = %s
            ON CONFLICT DO NOTHING;
            """
        # IP.embed()
        for obs in obses:
            if not obs['eoi'] == None:
                values = obs['values']
                for value in values:
                    data = (
                        obs['eoi'],
                        value['fromTime'],
                        value['toTime'],
                        value['value'],
                        obs['component'],
                    )
                    cur.execute(q, data)
        conn.commit()
        cur.close()
                

        
    def build_backlog_obs(self, timedelta_days=20, dateTo=datetime.date(2019, 11, 1)):
        today = datetime.date.today()
        timedelta = datetime.timedelta(days=timedelta_days)
        current_date = today
        print(f"current_date: {current_date}")
        while current_date > dateTo:
            self.update_obs_historical(current_date-timedelta, current_date)
            current_date = current_date - timedelta
        


   # show data

    def matrix_plot(self):
        pass


if __name__ == "__main__":
    tmp = air()
    # data = tmp.get_aq()
    # data = tmp.get_aq(utd=False, fromTime="2019-01-01", toTime="2019-01-03", station="alnabru")
    # tmp.update_stations_db()


    # today = datetime.date.today()
    # timedelta = datetime.timedelta(days=20)
    # fromTime = today - timedelta

    tmp.build_backlog_obs()

    IP.embed()
