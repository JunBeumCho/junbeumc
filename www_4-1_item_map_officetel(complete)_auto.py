#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import unittest
import datetime
import random
import sys, traceback
import telegram

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class detail_officetelTest(unittest.TestCase):

    def __init__(self, x):
        super().__init__()
        self.x = x

    def moveTab(self, x):
        window_before = self.driver.window_handles[x]
        self.driver.switch_to.window(window_before)
        return time.sleep(2)

    def setUp(self):
        self.chromeDriver = PATH('/Users/cell/Downloads/chromedriver')
        self.driver = webdriver.Chrome(executable_path=self.chromeDriver)
        self.wait = WebDriverWait(self.driver, 5)

    def runTest(self):
        count = 0
        while True:
            try:
                my_token = "729314656:AAFulVrBg4MQcEDBHi_oSUoIV1B2kPP0fIU"
                my_bot = telegram.Bot(token=my_token)
                zigbangUrl = "https://www.zigbang.com/"

                confirmAccount = "dustls456@naver.com"
                confirmpwAccount = "asd12345@"

                locations = ["강남구 역삼동", "성남시 정자동"]
                randomLocations = random.choice(locations)
                map_input_xpath = "//*[@id='__next']/div[2]/div/div[1]/div/div[3]/div[1]/div[1]/div/div[1]/input"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 오피스텔 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[3]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "오피스텔 찾기"))).click()
                time.sleep(1)

                # 2. 오피스텔 지도 화면 > 지하철역 검색

                self.wait.until(EC.visibility_of_element_located((By.XPATH, map_input_xpath))).send_keys(u"강남역")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-search"))).click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-clear "))).click()
                time.sleep(1)

                # 3. 오피스텔 지도 화면 > 오피스텔 검색

                self.wait.until(EC.visibility_of_element_located((By.XPATH, map_input_xpath))).send_keys(u"강남역센트럴푸르지오시티")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-clear "))).click()
                time.sleep(1)

                # 4. 오피스텔 지도 화면 > 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.XPATH, map_input_xpath))).send_keys(randomLocations)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-clear "))).click()
                time.sleep(1)

                break

            except Exception as e:
                err_msg = u"오피스텔 지도 페이지 오류:" + "\n" + str(e) + "\n\n" + self.driver.current_url

                if count == 2:
                    my_bot.sendMessage(chat_id='@zigbang_qa_notification', text=err_msg)
                    break

                else:
                    traceback.print_exc(file=sys.stdout)
                    self.driver.quit()
                    self.setUp()
                    count += 1

    def tearDown(self):
        self.driver.quit()