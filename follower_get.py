from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import sys
import csv
import datetime
import time
from dotenv import load_dotenv
load_dotenv()

import os
token = os.getenv('TOKEN')
path = os.getenv('FILEPATH')

## scraping the follower number
driver = webdriver.Chrome(executable_path = path)
driver.get("https://www.instagram.com/kaoru.m.0520/")
time.sleep(3)

element = driver.find_elements(By.CLASS_NAME,'_ac2a')
follower = element[1].get_attribute("title")
print('follower: ' + follower)

## add and write to a csv file
csv_file_name = "mitoma.csv"
f = open(csv_file_name, mode = 'a', encoding='cp932', errors='ignore')
writer = csv.writer(f, lineterminator='\n')
csvlist = []
today = datetime.datetime.now()
csvlist.append(today)
csvlist.append(follower)
writer.writerow(csvlist)

f.close()
## send to LINE
message = 'フォロワー数:' + follower

def send_line_notify(notification_message):
        line_notify_token = token
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': f'message: {message}'}
        requests.post(line_notify_api, headers = headers, data = data)

send_line_notify(message)    