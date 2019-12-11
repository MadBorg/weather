import pandas as pd

import weather

class stations:
    path =  "stations.json"
    def __init__(self):
        self.df = pd.read_json(self.path)

    def get_komuner():
        pass