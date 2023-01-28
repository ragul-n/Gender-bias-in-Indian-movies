import time
import re
import pandas as pd
import time
import json
import requests
from bs4 import BeautifulSoup
import tqdm

from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def init_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
    })                  

    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    chrome_options.add_argument("user-data-dir=C:/Users/natar/AppData/Local\Google/Chrome/User Data/Profile 1") 


    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    driver = webdriver.Chrome("C:\DRIVERS\chromedriver.exe",options=chrome_options,desired_capabilities=capabilities)
    driver.implicitly_wait(10)

    return driver


def get_data_from_card(card):
    h2s= card.find_elements_by_tag_name("h2")
    title= h2s[0].text if len(h2s)>0 else None
    span_list= card.find_elements_by_tag_name("span")
    span_list=[i.text for i in span_list]

    if len(span_list)==4:
        type,language,year,ott=span_list
    elif len(span_list)==3:
        type,language,year= span_list
        ott=pd.NA
    else:
        language,year,ott='None','None',pd.NA

    return {
        "title":title,
        "language":language,
        "year":year,
        "ott":ott
    }

def check_match(x, y):
    """
    Args:
        x (dict): movie data (actual)
        y (dict): scraped data

    Returns:
        bool: Ture if data matches
    """
    if y["language"].lower() in ("english",x["Language"]):
        if (x['Movie Name'].lower(), x['Year'])==(y["title"].lower(),y["year"]):
            return True
        

def get_ott(driver, movie_data):
    cards=driver.find_elements_by_class_name("searchNew_searchList__items__S25cq")
    for card in cards:
        scraped_data=get_data_from_card(card)
        if check_match(movie_data, scraped_data):
            return scraped_data["ott"]
    else:
        return pd.NA


def scrape_data(data):
    for i,movie_data in tqdm.tqdm(list(data.iterrows())):
        driver.get("https://www.ottplay.com/search?query={}".format(movie_data["Movie Name"].replace(" ","+")) )
        time.sleep(0.5)
        movie_data["ott"]=get_ott(driver, movie_data)
        movie_data.to_frame().T.to_csv("data/ott_data.csv",index=False, header=False, mode="a")
        

if __name__=="__main__":

    movies_data=pd.read_csv("C:\Projects\Gender-bias-in-Indian-cinema\Gender-bias-in-Indian-cinema\Data Collection\data\indian movies.csv")
    movies_data["Year"]= movies_data.Year.str.extract("(\d{4})").loc[:,0]
    movies_data["Year"]=[i for i in movies_data.Year]

    driver=init_driver()

    scrape_data(movies_data.iloc[len(pd.read_csv("ott_data.csv", header=None))+1:])
