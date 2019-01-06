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
            icon, summary = get_forecast(cfg)
            render(icon, summary)
    except IOError as error:
        logger.info("No config file found")
        render("fail", "No config file")
    except requests.ConnectionError:
        logger.info("Connection Error")
        render("fail", "Connection Error")
    except ValueError:
        logger.info("Connection Error")
        render("fail", "Value Error")


def get_forecast(cfg):
    logger.info("fetching forecast")
    url = API_URL % (cfg['api'], cfg['lat'], cfg['lon'])
    r = requests.get(url)
    data = r.json()
    icon = data['currently']['icon']
    summary = data['hourly']['summary']
    return (icon, summary)
