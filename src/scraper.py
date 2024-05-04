import requests
from bs4 import BeautifulSoup
import datetime
import re
import utils
import selenium
from selenium import webdriver



def get_soup(url):
    """Fetch a webpage and return a BeautifulSoup object."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'lxml')
    else:
        return None





if __name__ == "__main__":
