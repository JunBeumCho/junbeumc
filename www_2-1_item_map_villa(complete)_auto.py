#-*- coding: utf-8 -*-
import random

from selenium import webdriver
import os
import time
import pdb
import unittest
import sys, traceback

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class item_map_villaTest(unittest.TestCase):

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
                random_regions = random.choice(["양천구", "송파구", "한남동", "강남구"])
                random_stations = random.choice(["강남구청역", "학동역", "사당역", "오금역"])

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.maximize_window()

                # 1. 빌라 지도화면 이동

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[1]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "빌라, 투룸 찾기"))).click()
                time.sleep(2)

                # 2. 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-wrap > #test"))).send_keys(random_regions)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".search-result-container > .select-options-wrap > .select-item")))[0].click()
                time.sleep(7)

                location_name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".title_a > .title"))).text

                if not "이 지역 매물 목록" == location_name:
                    raise Exception(u"매물 목록이 정상적으로 노출되고 있지 않음")

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-wrap > .btn-clear"))).click()

                # 3. 지하철역 검색

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-wrap > #test"))).send_keys(random_stations)

                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".search-result-container > .select-options-wrap > .select-item")))[0].click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-wrap > .btn-clear"))).click()

                # 4. 빌라 실거래가 마커 뜨고 없어지는지 확인
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btnPriceMarker"))).click()
                time.sleep(3)

                # -> 실거래가 마커가 사라지는거 확인

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btnPriceMarker"))).click()
                time.sleep(7)
                # -> 실거래가 마커가 다시 나타나는지 확인

                # 5. 빌라 실거래가 매물 상세 클릭 및 뒤로가기
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-wrap > #test"))).send_keys("영천시 도동")
                self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".search-result-container > .select-options-wrap > .select-item")))[0].click()
                time.sleep(3)

                # 실거래가 마커 클릭
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#react-villaMap .villa-map-area .priceMarker"))).click()
                time.sleep(7)

                # 실거래가 창에 5개의 표가 모두 뜨는지 확인
                #for i in range(6):
                    #print(self.driver.find_elements_by_css_selector(".villa-layer-content .fyervv")[i])
                    #if self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".villa-layer-content .fyervv[i]"))) is None:
                    #    raise Exception(u"실거래가 화면이 작동 안됨")

                address = self.driver.find_element_by_css_selector("div.villa-layer-content > div > div:nth-child(1) > div > div > h3").text
                info_table = self.driver.find_element_by_css_selector("div.villa-layer-content > div > div:nth-child(2) > div > div.i-title > div").text
                family_info = self.driver.find_element_by_css_selector("div.villa-layer-content > div > div:nth-child(3) > div > div.i-title > div").text
                school_info = self.driver.find_element_by_css_selector("div.villa-layer-content > div > div:nth-child(4) > div > div.i-title > div").text
                traffic_info = self.driver.find_element_by_css_selector("div.villa-layer-content > div > div:nth-child(5) > div > div > div.i-title > div:nth-child(1)").text
                location_info = self.driver.find_element_by_css_selector("div.villa-layer-content > div > div:nth-child(6) > div > div.i-title > div").text

                if not (address == u"천마빌라(영천시 도동 511-1)"):
                    raise Exception(u"실거래가 주소가 노출이 안되고 있음")

                if not (info_table == u"실거래 정보"):
                    raise Exception(u"실거래가 실거래 정보 노출이 안되고 있음")

                if not (family_info == u"세대 정보 (총 12세대)"):
                    raise Exception(u"실거래가 세대 정보 노출이 안되고 있음")

                if not (school_info == u"학군 정보"):
                    raise Exception(u"실거래가 학군 정보 노출이 안되고 있음")

                if not (traffic_info == u"교통 정보"):
                    raise Exception(u"실거래가 교통 테이블 노출이 안되고 있음")

                if not (location_info == u"위치"):
                    raise Exception(u"실거래가 위치 노출이 안되고 있음")


                break



            except Exception as e:
                err_msg = u"빌라 지도 페이지 오류:" + "\n" + str(e) + "\n\n" + self.driver.current_url

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