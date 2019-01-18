#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import unittest
import random
import datetime
import sys, traceback
import telegram

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class detail_oneroomTest(unittest.TestCase):

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

                confirmAccount = "qa_test_account2@gmail.com"
                confirmpwAccount = "Wlrqkd7905!"

                randomstations = random.choice(["수원역", "홍대입구역", "서울대입구역", "건대입구역"])
                VIPstations = random.choice(["신림역", "수지구청역"])

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 원,투룸 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[2]
                ActionChains(self.driver).move_to_element(element_to_hover_over).perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"방 찾기"))).click()
                time.sleep(2)



                # 2. 원룸 지도 화면 > 지하철역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(randomstations)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                stationName = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".list-title > h3"))).text

                if not randomstations == stationName:
                    raise Exception(u"역이름이 일치하지 않습니다.", stationName)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                # 3. 원룸 지도 화면 > 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(u"서울시 동작구 사당동")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                # VIP 태그 확인

                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys(VIPstations)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-delete"))).click()
                time.sleep(1)

                for i in range(4):
                    if self.driver.find_elements_by_class_name("itemAgentBox")[i] is None:
                        raise Exception(u"VIP 중개사 갯수 노출 오류")

                # 매물 상단바가 잘 노출 되는지 확인
                if not self.driver.find_elements_by_css_selector("map-list-scroll > h4:nth-child(1)") == self.driver.find_elements_by_css_selector("map-list-scroll > .list-tit .vip"):
                    raise Exception(u"안심중개사 VIP 매물 상단바가 제대로 노출되고 있지 않습니다.")

                if not self.driver.find_elements_by_css_selector("map-list-scroll > h4:nth-child(2)") == self.driver.find_elements_by_css_selector("map-list-scroll > .list-tit .premium_special"):
                    raise Exception(u"안심중개사 추천 매물 상단바가 제대로 노출되고 있지 않습니다.")

                # 매물 목록이 잘 노출 되는지 확인
                if not self.driver.find_elements_by_css_selector("map-list-scroll > div:nth-child(1)") == self.driver.find_elements_by_css_selector("map-list-scroll > .m-list .vip-list"):
                    raise Exception(u"안심중개사 VIP 매물 목록이 제대로 노출되고 있지 않습니다.")

                if not self.driver.find_elements_by_css_selector("map-list-scroll > div:nth-child(2)") == self.driver.find_elements_by_css_selector("map-list-scroll > .m-list .premium-special-list"):
                    raise Exception(u"안심중개사 추천 매물 목록이 제대로 노출되고 있지 않습니다.")

                break

            except Exception as e:
                err_msg = u"원룸 지도 페이지 오류:" + "\n" + str(e) + "\n\n" + self.driver.current_url

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