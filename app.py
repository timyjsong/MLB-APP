"""
    Module for MLB-APP
"""
import os
import json
import requests
from bs4 import BeautifulSoup

from logger import LOGGER

LOGGER = LOGGER.get_logger("app")


def parse_json(url):
    """ Parsing espn json from url """
    LOGGER.info(f"GET {url}")

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    for script in soup.findAll("script"):
        if "__espnfitt__" in str(script):
            found = script.text
            break

    espn_data = found.replace("window['__espnfitt__']=", "")[:-1]
    return json.loads(espn_data)


def overwrite_cache(file_path, url):
    dirpath = os.path.sep.join(file_path.split(os.path.sep)[:-1])
    os.makedirs(dirpath, exist_ok=True)
    espn_json = parse_json(url)
    with open(file_path, "w") as f:
        json.dump(espn_json, f)
    return espn_json


def cache_loader(file_path, url, force_reload=False):
    if force_reload is False:
        try:
            with open(file_path, "r") as f:
                espn_json = json.load(f)
        except FileNotFoundError:
            LOGGER.info(f"Cache Miss: {file_path}")
            espn_json = overwrite_cache(file_path, url)
        else:
            LOGGER.info(f"Cache Hit: {file_path}")
    else:
        LOGGER.info("Cache Reload")
        espn_json = overwrite_cache(file_path, url)

    return espn_json


def main():
    url = "https://www.espn.com/mlb/teams"
    espn_json = cache_loader("cache/mlb.json", url)


if __name__ == "__main__":
    main()
