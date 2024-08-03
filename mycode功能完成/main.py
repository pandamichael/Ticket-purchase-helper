import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import re
import os
from datetime import datetime
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from PyQt5.QtWidgets import QWidget
from View.v_1223_ui_5 import *
from Model.m_1223_ui_5 import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from json import loads, dumps
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import ddddocr
from PIL import Image
import urllib
import cv2
import numpy as np
from selenium.webdriver.support.ui import Select

# 獲取當前腳本所在的目錄
current_directory = os.path.dirname(os.path.abspath(__file__))
# ChromeDriver的相對路徑
chrome_driver_path = os.path.join(current_directory, 'chromedriver.exe')


class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleCalc)
        self.comboBox_2.currentIndexChanged.connect(self.handleComboBoxChange)



    def handleCalc(self):
        url = self.textEdit.toPlainText()
        if not self.is_valid_url(url):
            self.show_message("網址錯誤", "請輸入有效的網址")  # 若輸入非有效網址，則跳出提示視窗
            return

        self.open_url_and_click_button(url)

    def handleComboBoxChange(self, index):
        selected_session = self.comboBox_2.currentText()  # 獲取使用者輸入的場次資訊
        if selected_session:
            self.process_selected_session(selected_session)

    def is_valid_url(self, url):
        # 驗證輸入的是否為有效網址
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
            r'localhost|' 
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def open_url_and_click_button(self, url):
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            print(f"已打開網址: {url}")
            driver.maximize_window()

            try:
                accept_cookies_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
                )
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
                )
                accept_cookies_button.click()
            except Exception as e:
                print("找不到允許 Cookie 的按鈕，或者頁面上沒有彈窗。")

            login_button = driver.find_element(By.XPATH, "//*[@id='bs-navbar']/div/div[2]/ul[3]/li/a")
            login_button.click()
            time.sleep(1)

            google_login = driver.find_element(By.XPATH, "//a[contains(@href, 'https://tixcraft.com/login/google')]")
            google_login.click()
            time.sleep(1)

            username_input = driver.find_element(By.ID, "identifierId")
            username_input.send_keys("pythonccclubproject@gmail.com") 
            next_button = driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button")
            next_button.click()
            time.sleep(3)

            password_input = driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
            password_input.send_keys("Pythonccclub")  
            password_input.send_keys(Keys.RETURN)
            time.sleep(1)

            user_time = self.timeEdit.time().toString("HH:mm:ss")
            target_time = datetime.strptime(user_time, "%H:%M:%S").time()
            print(f"目標時間：{target_time}")

            while datetime.now().time() < target_time:
                print("等待目標時間...")
                time.sleep(1)

            print("到達目標時間，繼續執行...")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tab-func"]/li[1]/a/div'))
            )

            elem_operate_1 = driver.find_element(By.XPATH, '//*[@id="tab-func"]/li[1]/a/div')
            driver.execute_script("arguments[0].click();", elem_operate_1)
            print("成功點擊了第一個元素")
            time.sleep(1)

            session_buttons = driver.find_elements(By.XPATH, '//*[@id="gameList"]//button')
            num_sessions = len(session_buttons)
            print(f"找到 {num_sessions} 個場次按鈕")

            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

            selected_session = self.comboBox_2.currentText()
            print(f"選擇的場次：{selected_session}")
            session_number = self.extract_session_number(selected_session)
            print(f"提取的場次號碼：{session_number}")
            if session_number is not None:    #檢查提取到的場次是否有效
                if 1 <= session_number <= num_sessions:
                    target_button = session_buttons[session_number - 1]
                    print(f"嘗試點擊第 {session_number} 個場次按鈕")
                    driver.execute_script("arguments[0].scrollIntoView();", target_button)
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="gameList"]//button'))
                    )
                    target_button.click()
                    print(f"成功點擊了第 {session_number} 個場次按鈕")

                    user_input = self.textEdit_4.toPlainText()
                    if user_input.isdigit():
                        user_number = int(user_input)
                        print(f"用戶輸入的數字：{user_number}")             

                    try:
                        zone_area_list_divs = driver.find_elements(By.XPATH, '//div[@class="zone area-list"]')
                        user_input = self.textEdit_4.toPlainText().strip()
                        user_input_6 = self.textEdit_6.toPlainText().strip()
                        print(f"使用者輸入的排除字：{user_input_6}")

                        for div in zone_area_list_divs:
                            ul_tags = div.find_elements(By.TAG_NAME, 'ul')
                            for ul in ul_tags:
                                print(f"找到的區域文本內容：{ul.text}")

                                # 迭代 ul 中的每个 li 元素，检查是否包含用户输入的任何部分
                                for li in ul.find_elements(By.TAG_NAME, 'li'):
                                    area_text = li.text.strip()
                                    if user_input in area_text and user_input_6 not in area_text:
                                        try:
                                            # 將目標 li 元素滾動到視窗內可見範圍
                                            driver.execute_script("arguments[0].scrollIntoView();", li)
                                            time.sleep(0.5)  # 可選擇性的等待0.5秒鐘，確保元素完全加載和滾動完成

                                            # 創建 ActionChains 物件，將滑鼠移動到目標元素上並點擊
                                            actions = ActionChains(driver)
                                            actions.move_to_element(li)
                                            actions.click().perform()
                                            print(f"成功點擊了符合條件的 li 元素：{area_text}")
                                            time.sleep(0.5)
                                            
                                            # 在這裡放置選擇張數的操作
                                            WebDriverWait(driver, 10).until(
                                                EC.presence_of_element_located((By.XPATH, '//*[@id="TicketForm_ticketPrice_01"]'))
                                            )

                                            # 在新頁面上進行後續操作，例如選擇張數
                                            selected_value = self.comboBox.currentText()
                                            user_number = int(selected_value)
                                            how_many_tickets = driver.find_element(By.XPATH, '//*[@id="TicketForm_ticketPrice_01"]')
                                            select = Select(how_many_tickets)
                                            select.select_by_value(value=str(user_number))

                                            # 網頁截圖
                                            try:
                                                screenshot_path = os.path.join(current_directory, "screenshot.png")
                                                driver.save_screenshot(screenshot_path)

                                                if os.path.exists(screenshot_path):
                                                    print(f"Screenshot saved successfully at {screenshot_path}")
                                                else:
                                                    raise FileNotFoundError("Failed to save screenshot")

                                                # 打開原始截圖
                                                screenshot = Image.open(screenshot_path)

                                                # 定義驗證碼圖片的區域
                                                left = 730
                                                top = 635
                                                right = 845
                                                bottom = 730

                                                # 擷取驗證碼區域
                                                captcha_image = screenshot.crop((left, top, right, bottom))

                                                # 保存擷取的驗證碼圖片
                                                captcha_image_path = os.path.join(current_directory, 'captcha.png')
                                                captcha_image.save(captcha_image_path)

                                                print(f"驗證碼圖片已保存到 {captcha_image_path}")
                                                time.sleep(1)

                                                # 初始化 ddddocr
                                                ocr = ddddocr.DdddOcr()

                                                # 載入圖片
                                                with open(captcha_image_path, 'rb') as f:
                                                    image_bytes = f.read()

                                                # 驗證碼識別
                                                result = ocr.classification(image_bytes)

                                                print(f'Recognized text: {result}')

                                                # 進行驗證碼輸入
                                                input_captcha = driver.find_element(By.XPATH, '//*[@id="TicketForm_verifyCode"]')
                                                input_captcha.send_keys(result)
                                                time.sleep(0.5)

                                                # 點選"我同意"
                                                accept = driver.find_element(By.XPATH, '//*[@id="TicketForm_agree"]')
                                                accept.click()
                                                time.sleep(0.5)

                                                # 提交
                                                confirm = driver.find_element(By.XPATH, '//*[@id="form-ticket-ticket"]/div[4]/button[2]')
                                                confirm.click()
                                                time.sleep(600)

                                            except FileNotFoundError as e:
                                                print(f"文件保存錯誤：{str(e)}")
                                            except NoSuchElementException as e:
                                                print(f"找不到元素：{str(e)}")
                                            except Exception as e:
                                                print(f"操作發生錯誤：{str(e)}")

                                        except NoSuchElementException as e:
                                            print(f"找不到符合條件的 li 元素：{str(e)}")
                                            # 可添加其他处理逻辑，如重新尝试点击等
                                        except Exception as e:
                                            print(f"操作发生错误：{str(e)}")

                                                                   
                    except TimeoutException as e:
                        print(f"等待元素超时：{str(e)}")
                    except NoSuchElementException as e:
                        print(f"找不到元素：{str(e)}")
                    except Exception as e:
                        print(f"操作发生错误：{str(e)}")


                    
                    

                else:
                    print("選擇的場次超出範圍")
            else:
                print("無法提取場次號碼")

        except TimeoutException as e:
            print(f"等待新頁面元素超時：{str(e)}")
            self.show_message("錯誤", f"等待新頁面元素超時：{str(e)}")
        except NoSuchElementException as e:
            print(f"找不到元素：{str(e)}")
            self.show_message("錯誤", f"找不到元素：{str(e)}")
        except Exception as e:
            print(f"操作過程中發生錯誤：{str(e)}")
            self.show_message("錯誤", f"操作過程中發生錯誤：{str(e)}")
    
    def process_selected_session(self, selected_session):
        print(f"選擇的場次: {selected_session}")

    def chinese_to_arabic(self, chinese_num):
        chinese_to_arabic_dict = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, 
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        result = 0
        for char in chinese_num:
            if char in chinese_to_arabic_dict:
                result = result * 10 + chinese_to_arabic_dict[char]
        return result

    def extract_session_number(self, selected_session):
        match = re.search(r'\d+', selected_session)
        if match:
            return int(match.group())
        else:
            return self.chinese_to_arabic(selected_session)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())