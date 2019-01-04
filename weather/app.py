import requests
import json
from weather.display import render

API_URL = 'https://api.darksky.net/forecast/%s/%s,%s'
CONFIG_FILE = './config.json'


def validateConfig(cfg):
    pass


def main():

    try:
        with open(CONFIG_FILE) as json_data_file:
            cfg = json.load(json_data_file)
            validateConfig(cfg)
            start(cfg)
    except IOError as error:
        print("No config file found")
        render("fail", "No config file")
    except ValueError as error:
        print(error)


def start(cfg):
    try:
        forecast = get_forecast(cfg)
        icon = forecast['currently']['icon']
        summary = forecast['hourly']['summary']

    except requests.ConnectionError:
        print("Connection Error")
        forecast = "fail"
    finally:
        render(icon, summary)


def get_forecast(cfg):
    print("fetching forecast")
    url = API_URL % (cfg['api'], cfg['lat'], cfg['lon'])
    r = requests.get(url)
    data = r.json()
    return data
