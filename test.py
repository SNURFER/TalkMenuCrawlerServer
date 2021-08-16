import selenium, os, shutil, time, pandas
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

#parse xlsx with pandas 
menuSheet = pandas.read_excel(newFileName, sheet_name=0, engine='openpyxl')

totalRow = menuSheet.shape[0] - 1
print(menuSheet)

bldIdx = []
menuIdx = []

for row in menuSheet.itertuples():
    if (pandas.isnull(row[1]) == False):
        bldIdx.append(row[0])
    if (pandas.isnull(row[2]) == False):
        menuIdx.append(row[0])
        
print('breakfast lunch dinner start idx')
print(bldIdx)
print('---------')
print('menu start idx')
print(menuIdx)

# mon tue wed thu fri
# breakfast lunch dinner
menuTable = [[0 for i in range(5)] for j in range(3)]
for i in range(0, 5): 
    bStr = ""
    lStr = "" 
    dStr = "" 
    for row in menuSheet.itertuples():
        if (bldIdx[1] <= row[0] and row[0] < bldIdx[2] and pandas.isnull(row[i + 3]) == False):
            bStr += row[i + 3] + '\n'
        if (bldIdx[2] <= row[0] and row[0] < bldIdx[3] and pandas.isnull(row[i + 3]) == False):
            lStr += row[i + 3] + '\n'
        if (bldIdx[3] <= row[0] and row[0] < totalRow and pandas.isnull(row[i + 3]) == False):
            dStr += row[i + 3] + '\n'
    menuTable[0][i] = bStr
    menuTable[1][i] = lStr
    menuTable[2][i] = dStr

print('friday print test')
print('br')
print(menuTable[0][3])
print('lu')
print(menuTable[1][3])
print('di')
print(menuTable[2][3])
