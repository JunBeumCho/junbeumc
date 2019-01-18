#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import unittest
import sys, traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import telegram

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class item_zzimTest(unittest.TestCase):

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

                confirmAccount = "qa_test_account@gmail.com"
                confirmpwAccount = "Wlrqkd7905!"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 찜한 방 접속

                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[2]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "찜한 매물"))).click()
                time.sleep(1)

                # 2. 로그인 버튼 클릭

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(confirmAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(confirmpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                # 3. 찜 매물 개수 확인

                zzimList = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item"))))

                zzimCount = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-title > span"))).text
                zzimReplace = zzimCount.replace("(", "").replace(")", "")

                if not int(zzimList) == int(zzimReplace):
                    raise Exception("찜 개수가 상이함으로 자동화를 종료합니다.", "찜 리스트 : ", int(zzimList), "찜 개수 표시 : ", int(zzimReplace))

                # 4. 찜목록 불러오기 확인

                if int(zzimReplace) != 1:
                    raise Exception("찜목록을 가져올 수 없습니다.")


                # 5. 임의의 방 찜 목록 등록

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[2].click()
                time.sleep(2)

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item")))[0].click()
                self.moveTab(1)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.btn_bx > button.btn-zzim.off"))).click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-layer > div > div > button"))).click()
                time.sleep(1)


                # 6. 전체 선택 및 전체 해제
                element_to_hover_over = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[2]
                hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
                hover.perform()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "찜한 매물"))).click()
                time.sleep(1)


                zzimList = len(self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item"))))

                zzimCount = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-title > span"))).text
                zzimReplace = zzimCount.replace("(", "").replace(")", "")

                if not int(zzimList) == int(zzimReplace):
                    raise Exception("찜 개수가 상이함으로 자동화를 종료합니다.", "찜 리스트 : ", int(zzimList), "찜 개수 표시 : ", int(zzimReplace))

                if int(zzimReplace) != 2:
                    raise Exception("찜목록을 가져올 수 없습니다.")

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "allcheck_btn1"))).click()
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"삭제"))).click()
                time.sleep(2)

                self.wait.until(EC.alert_is_present()).accept()
                time.sleep(2)


                # 7. 테스트방 찜 목록 추가

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "has_d2")))[2].click()
                self.wait.until(EC.visibility_of_element_located((By.ID, "rooms-textfield"))).send_keys("서도면")
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.ID, "btn-room-search"))).click()
                time.sleep(3)

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "list-item")))[0].click()
                self.moveTab(2)
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.btn_bx > button.btn-zzim.off"))).click()
                time.sleep(1)

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-layer > div > div > button"))).click()
                time.sleep(1)

                print("원룸/오피스탤 찜목록 완료")

                break

            except Exception as e:
                err_msg = u"원룸 찜목록 페이지 오류:" + "\n" + str(e) + "\n\n" + self.driver.current_url

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