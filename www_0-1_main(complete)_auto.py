#-*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import pdb
import unittest
import sys, traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class mainTest(unittest.TestCase):

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
        my_token = "729314656:AAFulVrBg4MQcEDBHi_oSUoIV1B2kPP0fIU"
        my_bot = telegram.Bot(token = my_token)

        count = 0
        while True:
            try:
                zigbangUrl = "https://www.zigbang.com/"

                illbanidAccount = "whwnsqja100@naver.con"
                confirmAccount = "whwnsqja100@naver.com"
                confirmpwAccount = "jJ@134625"
                agentAccount = "test0057@zigbang.com"
                agentpwAccount = "rkskek1234"

                # 0. 직방 웹페이지 접속

                self.driver.get(zigbangUrl)
                time.sleep(1)

                self.driver.add_cookie({'name': 'cookie_sms_app_down', 'value': 'true'})
                # 지도 앱 다운로드 팝업 쿠키 True 값 고정

                self.driver.maximize_window()

                # 1. 미인증 계정 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(illbanidAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                userName = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='i_user']"))).text

                if not u"조준범" == userName:
                    raise Exception(u"사용자 이름이 일치하지 않습니다.", userName)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_user"))).click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"로그아웃"))).click()

                # 2. 인증 계정 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(confirmAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[type='password']"))).send_keys(confirmpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                userName = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='i_user']"))).text

                if not u"조준범" == userName:
                    raise Exception(u"사용자 이름이 일치하지 않습니다.", userName)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_user"))).click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"로그아웃"))).click()

                # 3. 중개사 계정 로그인

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_login"))).click()

                self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(agentAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(agentpwAccount)

                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-ok']"))).click()

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_link"))).click()
                self.moveTab(1)
                self.driver.close()
                self.moveTab(0)

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "i_user"))).click()

                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"로그아웃"))).click()

                # 4. 원,투룸 지역 검색
                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_rooms"))).click()
                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u"양천구 목동")
                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(3)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(1)

                # 5. 원,투룸 지하철 검색
                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_rooms"))).click()
                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'강남역')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(3)

                stationName = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='list-title']")))[0].text[0:3]

                if not u"강남역" == stationName:
                    raise Exception(u"역이름이 일치하지 않습니다.", stationName)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 6. 오피스텔 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_officetel"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'직방테스트오피스텔')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(3)

                #officetel_name = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='list-title']")))[0].text[0:9]

                #if not u"직방테스트오피스텔" == officetel_name:
                #    raise Exception(u"오피스텔명이 일치하지 않습니다.", officetel_name)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 7. 아파트 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'강남역')
                time.sleep(1)
                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(5)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)


                # 8. 아파트 지하철 검색 (현재 버그여서 안되고 있음)

                #self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                #self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'용산구 한남동')
                #time.sleep(1)
                #self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                #time.sleep(5)

                #self.driver.execute_script("window.history.go(-1)")
                #time.sleep(2)

                #self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 9. 아파트 명 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_apartments"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'직방테스트1')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(3)

                #aptName = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='i-tit']"))).text[0:6]

                #if not u'직방테스트1' == aptName:
                #    raise Exception(u"아파트명이 일치하지 않습니다.", aptName)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 6. 빌라 지역 검색

                self.wait.until(EC.visibility_of_element_located((By.ID, "tit_villa"))).click()

                self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'방이동')

                self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(3)

                #officetel_name = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='list-title']")))[0].text[0:9]

                #if not u"직방테스트오피스텔" == officetel_name:
                #    raise Exception(u"오피스텔명이 일치하지 않습니다.", officetel_name)

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(2)

                self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 6. 빌라 지하철 검색 (현재 오류가 발생하고 있음)

                #self.wait.until(EC.visibility_of_element_located((By.ID, "tit_villa"))).click()

                #self.wait.until(EC.visibility_of_element_located((By.ID, "room-textfield"))).send_keys(u'사당역')

                #self.wait.until(EC.visibility_of_element_located((By.ID, "search_btn"))).click()
                time.sleep(3)

                ###officetel_name = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='list-title']")))[0].text[0:9]

                ###if not u"직방테스트오피스텔" == officetel_name:
                ###    raise Exception(u"오피스텔명이 일치하지 않습니다.", officetel_name)

                #self.driver.execute_script("window.history.go(-1)")
                #time.sleep(2)

                #self.wait.until(EC.visibility_of_element_located((By.ID, "delete_text"))).click()

                # 10. 중개사 가입 배너 클릭

                self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "m-tv"))).click()

                if not "https://www.zigbang.com/home/RegisterInfo" == self.driver.current_url:
                    raise Exception(u"CEO 페이지 링크가 잘못되었습니다")
                    # 이동 된 페이지 링크 검사

                self.driver.execute_script("window.history.go(-1)", self.driver.current_url)

                # 11. 뉴스 및 공지사항 더 보기 버튼 클릭
                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "item_more")))[0].click()

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(1)

                self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "item_more")))[1].click()

                self.driver.execute_script("window.history.go(-1)")
                time.sleep(1)

                break

            except Exception as e:

                err_msg = u"직방 메인 페이지 오류:" + "\n" + str(e) + "\n\n" + self.driver.current_url

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