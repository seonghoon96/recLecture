import requests as rq
import time
import pandas as pd
import openpyxl
import pymysql as pm
import sys
import os
import requests
import base64
import json
import logging
import time
import pandas as pd
import csv
from tabulate import tabulate
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_url = "http://www.hongik.ac.kr/login.do?Refer=https://cn.hongik.ac.kr/"  # 클래스넷 접속 URL
craw_url = 'https://cn.hongik.ac.kr/stud/' 

session = rq.session()

class Compares:

    def __init__(self, id, pw):
        self.params = dict()
        self.params['m_id'] = id  # 'B611090'
        self.params['m_passwd'] = pw  # 'titanic104404'
        self.check = dict()
        if id[0] == 'B':
            if int(id[1])<=8:
                self.check['졸업인정학점'] = [23,132]
                self.check['과학'] = 8
                self.check['수학'] = 9
                self.check['전산'] = 6
                self.check['계 (일반과정 MSC인정학점)'] = 18
                self.check['심화과정 MSC인정학점'] = 18
                self.check['전공'] = 54
                self.check['전공기초'] = 2
                self.check['취득학점'] = 132
        '''    elif int(id[1])<=8:
            else:
            
        elif id[0] == "C":
            if int(id[1]) <= 1:
        else:
        '''
        self.crawling()

    def crawling(self, ):

        # Selenium을 이용한 졸업요건 Crawling
        # 직접 클래스넷에 접속하여 졸업요건 조회 사이트로 이동
        # 이후 HTML 자체를 크롤링하여 졸업요건 Data 확보

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        chromedriver = '/Users/baekseunghoon/Desktop/pycharm/main/chromedriver' # 나중에 경로 어떻게 설정해야하는지 알아보고 수정할 것.
        driver = webdriver.Chrome(chromedriver, options=options)

        output = dict()
        # 홍익대학교 클래스넷 및 졸업요건조회 사이트로 이동

        driver.get(login_url)
        driver.find_element_by_name('USER_ID').send_keys(self.params.get('m_id'))
        driver.find_element_by_name('PASSWD').send_keys(self.params.get('m_passwd'))
        driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div[2]/div/table/tbody/tr/td[2]/div/form/div/div/div[2]/button').click()


        try:
            result = driver.switch_to.alert
            if result.text[:2] =='ID':
                return -1
            result.dismiss()
        except:
            "no"
        driver.get('https://cn.hongik.ac.kr/stud/E/04000/04000.jsp')
        driver.find_element_by_xpath('//*[@id="body"]/form/div[1]/table/tbody/tr/td[5]/input[2]').click()
        driver.find_element_by_xpath('//*[@id="body"]/form/div[2]/input[2]').click()


        # HTML crawling을 통한 User의 졸업요건 data 확보
        c = BeautifulSoup(driver.page_source, 'html.parser')
        c = c.find('div', class_="table0 mato10")
        info = driver.find_element_by_xpath('//*[@id="body"]/div[5]')
        info = info.find_elements_by_class_name("center")
        data = []

        # data가공
        for i in info:
            data.append(i.text)
        del data[0]
        del data[2]
        for idx, key in enumerate(data):
            if key == 'MSC':
                del data[idx]
                break
        data = data[:-4]
        Jcheck = 0
        cnt = 0
        ji = 0
        c = 0
        btncnt = 0
        for idx,key in enumerate(data):
            tmp = '-'
            if not key.isdigit():
                if key[0] == "일" or key[0] == "핵":
                    if key == '일반선택':
                        tmp = '-'

                    else:
                        if int(data[idx+1]) >=2:
                            cnt += 1
                            tmp = '충족'
                        else:
                            if cnt >= 6:
                                tmp = '부족(듣지 않아도 됨)'
                            else:
                                tmp = '부족'

                else:
                    if key in self.check:
                        if key == '졸업인정학점':
                            if self.check[key][ji] <= int(data[idx+1]):
                                tmp = '충족'
                            else:
                                tmp = '부족'
                            ji += 1
                        else:
                            if self.check[key] <= int(data[idx+1]):
                                tmp = '충족'
                            else:
                                tmp = '부족'
                if key == '졸업인정학점' and Jcheck == 0:
                    Jcheck +=1
                    c += 1
                    output['교양인정학점'] = ['교양','교양인정학점',int(data[idx+1]), tmp]
                else:
                    if c < 13:
                        if btncnt < 8:
                            output[key] = ['교양', key, int(data[idx + 1]), tmp,'btn']
                            btncnt += 1
                        else:
                            output[key] = ['교양',key,int(data[idx+1]),tmp]
                    elif c < 18:
                        if btncnt < 11:
                            output[key] = ['MSC', key, int(data[idx + 1]), tmp,'btn']
                            btncnt += 1
                        else:
                            output[key] = ['MSC',key,int(data[idx+1]),tmp]
                    else:
                        if btncnt < 13:
                            output[key] = ['-',key,int(data[idx+1]),tmp,'btn']
                            btncnt += 1
                        else:
                            output[key] = ['-', key, int(data[idx + 1]), tmp]
                    c+=1
        return output

