import data
import weather

class interface:
    def __init__(self):
        self.stations = data.stations()
        self.met = weather.met(weather.url)

    def search(self):
        stations = self.stations
        header = """
        Search options:
        """
        options = ["komune", "delområde", "name", "grunnkrets"]

        search_options = """"""
        for i in range(len(options)):
            search_options += f"{i+1}: {options[i]} \n"
        print(header)
        print(search_options)

        choice = options[int(input("Enter a number to choose option: "))-1]

        if choice == "name":
            station = self.search_name()
        import IPython; IPython.embed()
         
        print(self.met.get_data(station=station["eoi"]).json())
        
        
    def search_name(self):
        print("""
        1. Show options
        2. Just search
        """)
        choice = int(input("your choice: "))
        options = self.stations.df["name"]
        if choice == 1:  
            print("Places:")
            for i in range(len(options)):
                print(f"{i+1}: {options[i]}")
            chosen_name = int(input("Enter a number to choose option: "))-1
        else:
            chosen_name = int(input("Enter a number to choose option: "))-1
        return self.stations.df.iloc[chosen_name]
        
    

def run():
    while True:
        tmp = interface()
        tmp.search()


if __name__ == "__main__":
    run()