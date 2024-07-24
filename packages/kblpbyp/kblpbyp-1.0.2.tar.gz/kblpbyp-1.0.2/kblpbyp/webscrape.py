from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta, datetime
from plotnine import ggplot, aes, geom_point, geom_line, geom_vline, labs, theme_bw, theme, element_text, scale_x_continuous, scale_y_continuous, scale_color_manual, annotate, geom_ribbon, labs, element_blank, scale_size_identity
from sklearn.ensemble import RandomForestClassifier
# from dateutil import parser
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np
import re
import time
import requests

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

import sys
import itertools

import plotly.graph_objs as go

from collections import defaultdict
import math

driver = webdriver.Chrome()

def scrape(i, driver):

    if i == 5:
        element_css_selector = "a[href='#'][data-key='X1,X2,X3,X4,X5'"
        element = driver.find_element(By.CSS_SELECTOR, element_css_selector)
    else:
        element_css_selector = "a[href='#'][data-key='Q" + str(i) + "']"
        element = driver.find_element(By.CSS_SELECTOR, element_css_selector)

    # Click on the element using JavaScript
    driver.execute_script("arguments[0].click();", element)
    # Wait for 1 second
    time.sleep(1)
    # Get HTML content
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.con-box + .con-box td')))
    # Get the page source
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    message_elements = soup.select('.con-box + .con-box td')

    # Extract text from message elements
    message = [element.get_text() for element in message_elements]
    # Reverse the message list and create a dataframe
    message_df = pd.DataFrame({'Message': message[::-1]})

    return message_df

def cumulative_timedelta_sum(timedeltas):
    cumulative_sum = timedelta(0)
    cumulative_sums = []
    for td in timedeltas:
        cumulative_sum += td
        cumulative_sums.append(cumulative_sum)
    return cumulative_sums

def calculate_time_difference(times):
    time_differences = []
    for i in range(1, len(times)):
        difference = timedelta(hours=times[i-1].hour, minutes=times[i-1].minute, seconds=times[i-1].second) - \
                     timedelta(hours=times[i].hour, minutes=times[i].minute, seconds=times[i].second)
        if difference.total_seconds() < 0:
            difference = timedelta(seconds=0)
        time_differences.append(difference)
    return time_differences

def web_scrape_kbl(driver):
    column_names = ["team", "player_home_away", "time_remaining", "description"]

    # Create an empty DataFrame with column names
    empty_df = pd.DataFrame(columns=column_names)

    button = driver.find_element(By.CSS_SELECTOR, "li[data-key='onAirSms']")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    overtime = soup.select('.summary-table :nth-child(6)')
    overtime = [elem.get_text(strip=True) for elem in overtime]

    teams = soup.select('.info > h6')
    teams = [elem.get_text(strip=True) for elem in teams]

    date = soup.select('.bd-date')
    date = [elem.get_text(strip=True) for elem in date][0]
    date_string = date[:10]

    # Split the date string into components
    year, month, day = map(int, date_string.split('.'))
    date_object = datetime(year, month, day)
    formatted_date = date_object.strftime('%Y-%m-%d')

    total = soup.select('td:nth-child(7)')
    total = [elem.get_text(strip=True) for elem in total]

    time.sleep(1)

    if overtime[2] == "0" and overtime[3] == "0":
        for i in range(1, 5):
            message2 = scrape(i, driver)
            df = data_cleansing(message2)

            empty_df = pd.concat([empty_df, df], ignore_index=True)
    else:
        for i in range(1, 6):
            message2 = scrape(i, driver)
            df = data_cleansing(message2)

            empty_df = pd.concat([empty_df, df], ignore_index=True)

    empty_df['date'] = [formatted_date for _ in range(len(empty_df))]
    empty_df['team'] = np.where(empty_df['player_home_away'] == 'Home', teams[0], teams[1])

    if int(total[0]) - int(total[1]) > 0:
        empty_df['win_loss'] = [1 for _ in range(len(empty_df))]
    else:
        empty_df['win_loss'] = [0 for _ in range(len(empty_df))]
    return empty_df

def substr_right(x, n):
    return x[-n:]

def data_cleansing(data):
    kbl_pbp = pd.DataFrame(
        columns=['date', 'team', 'player_home_away', 'time_remaining', 'secs_remaining', 'play_length', 'description'])
    for i in range(len(data)):
        if bool(re.match("^-?\\d*\\.?\\d+$", data.iloc[i, 0][0])):
            kbl_pbp.loc[i, 'player_home_away'] = "Away"
            if bool(re.match("^10:00", data.iloc[i, 0][0:5])):
                kbl_pbp.loc[i, 'time_remaining'] = data.iloc[i, 0][0:5]
            else:
                kbl_pbp.loc[i, 'time_remaining'] = data.iloc[i, 0][0:4]

            time_pattern = r"^\d{1,2}:\d{2}"

            extracted_substring = re.sub(time_pattern + r'\s*', '', data.iloc[i, 0])

            extracted_substrings = re.sub(r'^\s+', '', extracted_substring)
            kbl_pbp.loc[i, 'description'] = extracted_substrings

        elif isinstance(data.iloc[i, 0][0:1], str):
            kbl_pbp.loc[i, 'player_home_away'] = "Home"
            trimmed_column = re.sub(r'^\s+', '', data.iloc[i, 0][-5:])
            kbl_pbp.loc[i, 'time_remaining'] = trimmed_column

            last_space_position = max(m.start() for m in re.finditer(' ', data.iloc[i, 0]))

            extracted_substring = data.iloc[i, 0][:last_space_position]

            extracted_substring = extracted_substring.lstrip()
            kbl_pbp.loc[i, 'description'] = extracted_substring

        # Cleaning the character values in the time_remaining column

    for i in range(1, len(kbl_pbp['time_remaining'])):
        if kbl_pbp.loc[i, 'time_remaining'].startswith('임시작 '):
            kbl_pbp.loc[i, 'time_remaining'] = kbl_pbp['time_remaining'][i - 1]
        elif kbl_pbp.loc[i, 'time_remaining'].startswith('임종료 '):
            kbl_pbp.loc[i, 'time_remaining'] = kbl_pbp['time_remaining'][i + 1]

    kbl_pbp['time_remaining'] = kbl_pbp['time_remaining'].str.replace('^칙', '', regex=True)

    return kbl_pbp

def data_cleansing2(pbp):
    quarter = 1
    pbp = pbp.reset_index(drop=True)
    for i in range(len(pbp) - 1):
        if pbp.loc[i, 'time_remaining'] == "0:00" and pbp.loc[i + 1, 'time_remaining'] != "0:00":
            pbp.loc[i, "quarter"] = quarter
            quarter = quarter + 1
        else:
            pbp.loc[i, "quarter"] = quarter

    # Finding the maximum quarter and assigning it to the last row
    pbp.loc[len(pbp) - 1, 'quarter'] = pbp['quarter'].max()
    pbp['quarter'] = pbp['quarter'].astype(int)
