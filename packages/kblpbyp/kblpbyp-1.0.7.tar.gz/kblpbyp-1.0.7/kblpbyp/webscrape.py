from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
import re
import time

# Initialize WebDriver
driver = webdriver.Chrome()


def scrape(i, driver):
    try:
        if i == 5:
            element_css_selector = "a[href='#'][data-key='X1,X2,X3,X4,X5']"
        else:
            element_css_selector = f"a[href='#'][data-key='Q{i}']"

        element = driver.find_element(By.CSS_SELECTOR, element_css_selector)
        driver.execute_script("arguments[0].click();", element)

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.con-box + .con-box td')))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        message_elements = soup.select('.con-box + .con-box td')
        message = [element.get_text() for element in message_elements]
        message_df = pd.DataFrame({'Message': message[::-1]})
        return message_df
    except Exception as e:
        print(f"Error in scrape function: {e}")
        return pd.DataFrame()


# Other functions remain unchanged...

def web_scrape_kbl(driver):
    column_names = ["team", "player_home_away", "time_remaining", "description"]
    empty_df = pd.DataFrame(columns=column_names)

    try:
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
    except Exception as e:
        print(f"Error in web_scrape_kbl function: {e}")
        return empty_df


# Add similar error handling and debugging in other functions...

def scrape_pbp_kbl_single(driver, starting_page):
    driver.get(starting_page)
    driver.refresh()
    time.sleep(2)

    KBL_PBP = pd.DataFrame()
    try:
        current_url = driver.current_url
        match = re.search(r"/record/(.*)$", current_url)
        game_id = match.group(1)
        print(f"Retrieving Game ID: {game_id}")

        pbp = web_scrape_kbl(driver)
        pbp = data_cleansing2(pbp)
        pbp = data_cleansing3(pbp)
        pbp['game_id'] = game_id
        KBL_PBP = pd.concat([KBL_PBP, pbp])
    except Exception as e:
        print(f"Error in scrape_pbp_kbl_single function: {e}")

    return KBL_PBP


