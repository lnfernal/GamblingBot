import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'http://app.prizepicks.com'
projections_xpath = '//*[@id="projections"]/div/div'


def get_button_xpath(button: str):
    button = button.lower()
    buttons = ['points', 'assists', 'rebounds', 'pts+rebs+asts', 'fantasy', '3pt', 'blks+steals']
    index = buttons.index(button) + 1

    return f'/html/body/div[2]/div/div[1]/div/div/div/main/div/div[2]/div/div[2]/div/div[{index}]'


def save_to_file(data, save_file='projections.json'):
    with open(save_file, 'w+') as f:
        data_json = json.dumps(data)
        f.write(data_json)


def main():
    buttons = ['points', 'assists', 'rebounds', '3pt']

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    welcome_message_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'getting-started-sounds-good-btn'))
    )
    welcome_message_button.click()

    projections = {}
    for button_name in buttons:
        xpath = get_button_xpath(button_name)
        button = driver.find_element(By.XPATH, xpath)

        button.click()

        data = gather_projections(driver)
        projections[button_name] = data

        time.sleep(1)

    save_to_file(projections)
    driver.quit()


def gather_projections(driver):
    elements = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'projection'))
    )

    bets = []
    for element in elements:
        score = element.find_elements(By.CLASS_NAME, 'presale-score')[0].get_attribute('innerHTML')
        name = element.find_elements(By.CLASS_NAME, 'name')[0].get_attribute('innerHTML')
        date = element.find_elements(By.CLASS_NAME, 'date')[0].get_attribute('innerHTML')
        text = element.find_elements(By.CLASS_NAME, 'text')[0].get_attribute('innerHTML')

        bet = {'player': name, 'value': score, 'type': text, 'date': date}
        bets.append(bet)

    return bets

if __name__ == '__main__':
    main()
