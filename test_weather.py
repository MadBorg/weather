import weather

url = "https://api.met.no/weatherapi/airqualityforecast/0.1/"


# does not chrash when used tests.
def test_weather_simple():
    test = weather.met(url)
    test.get_data(lat=59.9495395, lon=10.7201275)
    data = test.data
    # print(data)

def test_weather_stations():
    test = weather.met(url)
    stations = test.stations
    print(stations)

def test_weather_dump_data_to_file():
    test = weather.met(url)
    test.get_data(lat=59.9495395, lon=10.7201275)
    test.dump_data_to_file()

if __name__ == "__main__":
    # test_weather_simple()
    test_weather_stations()
    test_weather_dump_data_to_file()