import selenium, os, shutil, time, pandas, json
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.options import Options


filePath = os.getcwd() + '/downloads'

def init():

    #download path setting
    option = Options()
    option.add_experimental_option('prefs', {'download.default_directory' : filePath})

    #target url and http get
    URL = 'https://talk.tmaxsoft.com/login.do'
    driver = webdriver.Chrome(executable_path='chromedriver', options=option)
    driver.get(url=URL)

    #login
    userInfo = parseIdPw()
    driver.find_element_by_name('id').send_keys(userInfo[0])
    driver.find_element_by_name('pass').send_keys(userInfo[1])
    driver.find_element_by_id('loginPage_btn').click()

    return driver

#set of id/pw
def parseIdPw():
    userInfo = [0, 0]
    fd = open('input', 'r')
    lines = fd.readlines()
    for line in lines:
        if (line.find('id:') != -1):
            userInfo[0] = line[3:-1]
        if (line.find('pw:') != -1):
            userInfo[1] = line[3:-1]
    fd.close()

    return userInfo

def navigateAndDownload(driver):
    #macro event to download menu
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

    return newFileName

def parseXLSX(filePath):
    #parse xlsx with pandas 
    menuSheet = pandas.read_excel(filePath, sheet_name=0, engine='openpyxl')

    totalRow = menuSheet.shape[0] - 1
    # print(menuSheet)

    bldIdx = []
    menuIdx = []

    for row in menuSheet.itertuples():
        if (pandas.isnull(row[1]) == False):
            bldIdx.append(row[0])
        if (pandas.isnull(row[2]) == False):
            menuIdx.append(row[0])
            
    # print('breakfast lunch dinner start idx')
    # print(bldIdx)
    # print('---------')
    # print('menu start idx')
    # print(menuIdx)

    # mon tue wed thu fri
    # breakfast lunch dinner
    menuTable = [[0 for i in range(5)] for j in range(3)]
    for i in range(0, 5): 
        bStr = ""
        lStr = "" 
        dStr = "" 
        for row in menuSheet.itertuples():
            #breakfast
            if (bldIdx[1] <= row[0] and row[0] < bldIdx[2] and pandas.isnull(row[i + 3]) == False):
                bStr += row[i + 3] + '\n'
            #lunch
            if (bldIdx[2] <= row[0] and row[0] < bldIdx[3] and pandas.isnull(row[i + 3]) == False):
                lStr += row[i + 3] + '\n'
            #dinner
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
 
    menuJson = {
        "monday" : { 
            "breakfast" : menuTable[0][0],    
            "lunch" : menuTable[1][0],    
            "dinner" : menuTable[2][0],    
        }, 
        "tuesday" : {
            "breakfast" : menuTable[0][1],    
            "lunch" : menuTable[1][1],    
            "dinner" : menuTable[2][1],   
        },
        "wednesday" : {
            "breakfast" : menuTable[0][2],   
            "lunch" : menuTable[1][2],   
            "dinner" : menuTable[2][2],  
        },
        "thursday" : {
            "breakfast" : menuTable[0][3],  
            "lunch" : menuTable[1][3],    
            "dinner" : menuTable[2][3],   
        },
        "friday" : {
            "breakfast" : menuTable[0][4],   
            "lunch" : menuTable[1][4],   
            "dinner" : menuTable[2][4],    
        }
    }

    with open("menu.json", "w") as menu:
        json.dump(menuJson, menu)


if __name__ == '__main__':
    driver = init()
    downloadPath = navigateAndDownload(driver)
    parseXLSX(downloadPath)
    driver.close()
