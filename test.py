import selenium, os, shutil, time
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

#download path setting
filePath = os.getcwd() + '/downloads'
option = Options()
option.add_experimental_option('prefs', {'download.default_directory' : filePath})

#target url and http get
URL = 'https://talk.tmaxsoft.com/login.do'
driver = webdriver.Chrome(executable_path='chromedriver', options=option)
driver.get(url=URL)

#set of id/pw
fd = open('input', 'r')
lines = fd.readlines()
for line in lines:
 if (line.find('id:') != -1):
   userId = line[3:-1]
 if (line.find('pw:') != -1):
   userPw = line[3:-1]
fd.close()

#macro event to download menu
driver.find_element_by_name('id').send_keys(userId)
driver.find_element_by_name('pass').send_keys(userPw)
driver.find_element_by_id('loginPage_btn').click()
element = driver.find_element_by_css_selector('#menuLevelTop > li:nth-child(3) > a')
element.click()
driver.find_element_by_id('menuTM0012').click()
driver.find_element_by_id('listT0').click()

#download menu
element = driver.find_element_by_css_selector('#detailView0 > td > div > div > ul > li.boardBtnArea.borBottomEb > div > a')
element.click()

#rename menu
time.sleep(1)
newFileName = filePath + '/' + 'menu.xlsx'
fileName = max([filePath + '/' + f for f in os.listdir(filePath)], key=os.path.getctime)
shutil.move(os.path.join(filePath, fileName), newFileName)

