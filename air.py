import requests
import pandas as pd

class air:
    url = "https://api.nilu.no/aq/utd"

    def __init__(self):
        print(self.url)
    
    def gather_data(self):
        r = requests.get(self.url)
        data = r.json()
        for res in data:
            
        import IPython; IPython.embed()
    
   #show data
    
    def matrix_plot(self):
        pass

if __name__ == "__main__":
    tmp = air()
    tmp.gather_data()