from random import choice
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from json import loads, dumps
from db_maker import db_do, script_dir_finder
import time as TIME
import os
from datetime import timedelta
from all_config import getconfigs
import requests
import logging


def list_to_dict(data):
    new_data = loads(data)
    if "timestamp" in new_data:
        specs_json = dumps(new_data.get("specs", {}))
        histories_json = dumps(new_data.get("histories", {}))
        related_json = dumps(new_data.get("related", {}))
        flat_data = {
            "timestamp": new_data["timestamp"],
            "eventid": new_data["eventid"],
            "date": new_data["date"],
            "time": new_data["time"],
            "currency": new_data["currency"],
            "impact": new_data["impact"],
            "title": new_data["title"],
            "actual": new_data["actual"],
            "actualtype": new_data["actualtype"],
            "forecast": new_data["forecast"],
            "previous": new_data["previous"],
            "previoustype": new_data["previoustype"],
            "revised": new_data["revised"],
            "specs": specs_json,
            "histories": histories_json,
            "related": related_json
        }
        return flat_data
    else:
        return {
            "timestamp": None,
            "eventid": None,
            "date": None,
            "time": None,
            "currency": None,
            "impact": None,
            "title": None,
            "actual": None,
            "actualtype": None,
            "forecast": None,
            "previous": None,
            "previoustype": None,
            "revised": None,
            "specs": None,
            "histories": None,
            "related": None
        }


def insert_into_dataframe(dfAll, data_list):
    data_dicts = []
    data_dicts = list(map(list_to_dict, data_list))
    df = pd.DataFrame(data_dicts)
    dfAll = pd.concat([dfAll, df], ignore_index=True)
    dfAll.drop_duplicates("eventid", keep='last', inplace=True)
    return dfAll


def browser_options_maker():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    ]
    browser_options = webdriver.ChromeOptions()
    browser_options.add_argument("start-maximized")
    browser_options.add_argument("--log-level=3")
    user_agent = choice(user_agent_list)
    browser_options.add_argument(f'user-agent={user_agent}')
    return browser_options


def stamp_to_time(stamp):
    return timedelta(seconds=stamp)


def js_reader(name: str):
    script_dir = script_dir_finder()
    js_file = os.path.join(script_dir, name)
    with open(js_file, 'r') as reader:
        return reader.read()


def selenium_start():
    dfAll = pd.DataFrame()
    service = Service()
    browser_options = browser_options_maker()
    driver = webdriver.Chrome(options=browser_options, service=service)
    driver.get(URL)
    driver.delete_all_cookies()
    driver.set_script_timeout(300)
    if "Enable JavaScript and cookies to continue" in driver.page_source:
        logger.error("Enable JavaScript")
    driver.execute_script(DATA_SCRAPPER)
    upnext_timestamp = driver.execute_script(UPNEXT)
    driver.execute_script(CLICKER)
    return driver, dfAll, upnext_timestamp


def loop(driver, dfAll):
    dd = driver.execute_script(POP)
    if dd and len(dd) > 0:
        dfAll = insert_into_dataframe(dfAll, dd)
        json_file_name = CONFIGS['files']['temp']
        dfAll.to_json(json_file_name, orient='records')
        db_do(json_file_name)
    TIME.sleep(1)
    return dfAll


logger = logging.getLogger("my_logger")
logger.setLevel(logging.ERROR)


class ServerHandeler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        self.send_log_entry(log_entry)

    def send_log_entry(self, log_entry):
        url = f"https://api.telegram.org/bot{CONFIGS['telegram']['token']}/sendMessage?chat_id={CONFIGS['telegram']['chatid']}&text={log_entry}"
        requests.get(url)


logger.addHandler(ServerHandeler())


CONFIGS = getconfigs()
DATA_SCRAPPER = js_reader(CONFIGS['files']['data_scrapper'])
CLICKER = js_reader(CONFIGS['files']['clicker'])
POP = js_reader(CONFIGS['files']['pop'])
UPNEXT = js_reader(CONFIGS['files']['upnext'])
URL = CONFIGS['urls']['this_month']
driver, dfAll, upnext_timestamp = selenium_start()
while True:
    current_timestamp = int(TIME.time())
    dif = upnext_timestamp - current_timestamp
    print(f"next news in: {stamp_to_time(dif)}")
    if CONFIGS['times'].getint('six.thirty') <= dif <= CONFIGS['times'].getint('seven.thirty'):
        print("just before the news")
        break
    elif dif < CONFIGS['times'].getint('n.one.thirty'):
        print('after news')
        break
    else:
        dfAll = loop(driver, dfAll)
    #dfAll = loop(driver, dfAll)
    TIME.sleep(1)
driver.quit()
