""" Utils to return values from json.values """
import json
import logging
import os

def get_url_value() -> str:
    """ Should return url value from json.values """
    with open('values.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    try:
        return data['url_site']
    except ImportError as exception:
        logging.error(exception)

def get_chrome_driver_value() -> str:
    """ Should return chrome_driver value from json.values """
    with open('values.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    try:
        return data['chrome_drive']
    except ImportError as exception:
        logging.error(exception)

def get_output_dir_value() -> str:
    """ Should return csv_dir value from json.values """
    with open('values.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    try:
        return  os.path.abspath(data['output_dir'])
    except ImportError as exception:
        logging.error(exception)
        
def get_news_images_dir_value() -> str:
    """ Should return news_images_dir from json.values """
    with open('values.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    try:
        return data['news_images_dir']
    except ImportError as exception:
        logging.error(exception)
