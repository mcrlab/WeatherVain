import requests
import json
from weather.display import render
import logging

API_URL = 'https://api.darksky.net/forecast/%s/%s,%s'
CONFIG_FILE = './config.json'

logger = logging.getLogger('weather_application')

def validateConfig(cfg):
    pass


def main():

    try:
        with open(CONFIG_FILE) as json_data_file:
            cfg = json.load(json_data_file)
            validateConfig(cfg)
            start(cfg)
    except IOError as error:
        logger.info("No config file found")
        render("fail", "No config file")
    except ValueError as error:
        print(error)


def start(cfg):
    try:
        icon, summary = get_forecast(cfg)
    except requests.ConnectionError:
        logger.info("Connection Error")
        icon = "fail"
        summary = "Connection Error"
    except KeyError:
        icon = "fail"
        summary = "No forecast"
    finally:
        render(icon, summary)


def get_forecast(cfg):
    logger.info("fetching forecast")
    url = API_URL % (cfg['api'], cfg['lat'], cfg['lon'])
    r = requests.get(url)
    data = r.json()
    icon = data['currently']['icon']
    summary = data['hourly']['summary']
    return (icon, summary)
