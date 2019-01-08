import requests
import json
from weather.display import render
import logging
import datetime
import time
from weather.scheduler import Scheduler

API_URL = 'https://api.darksky.net/forecast/%s/%s,%s'
CONFIG_FILE = './config.json'
UPDATE_INTERVAL = 5
logger = logging.getLogger('weather_application')
last_update = None

def validateConfig(cfg):
    pass


def main():
    try:
        with open(CONFIG_FILE) as json_data_file:
            cfg = json.load(json_data_file)
            validateConfig(cfg)
            start_forecast_service(cfg)
    except IOError as error:
        logger.info("No config file found")
        render("fail", "No config file")


def start_forecast_service(cfg):
    try:
        while True:
            icon, summary = get_forecast(cfg)
            render(icon, summary)
            time.sleep(cfg['interval'])
            
    except KeyboardInterrupt:
        print('interrupted!')
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
