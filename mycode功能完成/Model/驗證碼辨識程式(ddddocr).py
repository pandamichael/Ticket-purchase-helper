import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import ddddocr
from PIL import Image
import urllib
import cv2
import numpy as np
import time
import os

# 設置Chrome選項
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#Options.add_experimental_option('detach', True)  #不要自動關閉selenium網頁

# 獲取當前腳本所在的目錄
current_directory = os.path.dirname(os.path.abspath(__file__))
# ChromeDriver的相對路徑
chrome_driver_path = os.path.join(current_directory, 'chromedriver.exe')

# 檢查ChromeDriver是否存在
if not os.path.exists(chrome_driver_path):
    print(f"ChromeDriver not found at {chrome_driver_path}")
    exit(1)

# 初始化ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://tixcraft.com/ticket/ticket/24_urboytj/17122/1/57"
print(f"Opening URL: {url}")
driver.get(url)
# 等待網頁加載完成，這邊秒數可調整
time.sleep(2)

# 選擇張數(與前面程式串接後可刪除)
how_many_tickets = driver.find_element(By.XPATH, '//*[@id="TicketForm_ticketPrice_01"]')
select = Select(how_many_tickets)
tickets = select.select_by_value(value = "2")

# 網頁截圖
screenshot_path = os.path.join(current_directory, "screenshot.png")
driver.save_screenshot(screenshot_path)                # 先將目前的 screen 存起來

# 檢查截圖是否成功保存
if os.path.exists(screenshot_path):
    print(f"Screenshot saved successfully at {screenshot_path}")
else:
    print("Failed to save screenshot")

# 打開原始截圖
screenshot = Image.open(screenshot_path)

# 定義驗證碼圖片的區域 (根據實際情況調整這些數值)
left = 590
top = 960
right = 765
bottom = 1095

# 擷取驗證碼區域
captcha_image = screenshot.crop((left, top, right, bottom))

# 保存擷取的驗證碼圖片
captcha_image_path = os.path.join(current_directory, "screenshot.png")
captcha_image.save(captcha_image_path)

print(f"驗證碼圖片已保存到 {captcha_image_path}")

# 初始化 ddddocr
ocr = ddddocr.DdddOcr()

# 載入圖片
image_path = 'screenshot.png'
with open(image_path, 'rb') as f:
    image_bytes = f.read()

# 驗證碼識別
result = ocr.classification(image_bytes)

print(f'Recognized text: {result}')

# 進行驗證碼輸入
input_captcha = driver.find_element(By.XPATH, '//*[@id="TicketForm_verifyCode"]')
input_captcha.send_keys(result)
time.sleep(2)
# try:
#     driver.switch_to_alert().accept() #若出現彈出視窗，點掉
# except Exception as e:
#     input_captcha.send_keys(result)
#     pass

#點選"我同意"
accept = driver.find_element(By.XPATH, '//*[@id="TicketForm_agree"]')
accept.click()
time.sleep(2)

#提交
confirm = driver.find_element(By.XPATH, '//*[@id="form-ticket-ticket"]/div[4]/button[2]')
confirm.click()
time.sleep(120)