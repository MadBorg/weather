import requests
import json
# import IPython; IPython.embed()
url = "https://api.met.no/weatherapi/airqualityforecast/0.1/"
class met:

   # special methods
    def __init__(self, url):
        self.url = url

   # private methods
    def _get_stations(self):
        arg = "stations/"
        r = self.get(argstr=arg)
        self._stations = self.parse(r)
        return self._stations

   #public methods
    def get(self, argstr):
        """
        TODO: format for json or xml
        """
        url = self.url + argstr
        r = requests.get(url)
        if r.ok: #test if response is ok
            self.r = r
            return r
        else: # if not raise exception
            raise Exception("response 400")
        # import IPython; IPython.embed()
        return self.r

    def get_data(self, **params):
        """
        TODO: format for json or xml
        """
        r = requests.get(self.url, params=params)
        if r.ok: #test if response is ok
            self.r = r
            return r
        else: # if not raise exception
            raise Exception("response 400")
        # import IPython; IPython.embed()
        return self.r
        
    def dump_data_to_file(self):
        """
        Comment:
            As implemented now, it takes json, parses it to python object for then to parse it to file. Wich is inefficient.
        """
        data = self.data
        self.json_to_file(data, "data.json")

   # properties
    @property
    def data(self):
        return self.parse(self.r)

    @property
    def stations(self):
        try:
            return self._stations
        except AttributeError:
            self._get_stations()
        return self._stations

   # static methods
    @staticmethod
    def parse(r):
        return r.json()

    @staticmethod
    def json_to_file(data, name="data.json", indent=4):
        with open(name, "w+") as f: #writing json object
            json.dump(data, f, indent= indent)

def update_stations_json(url):
    tmp = met(url)
    stations = tmp.stations
    tmp.json_to_file(stations, "stations.json", indent=2)

if __name__ == "__main__":
    update_stations_json(url)

