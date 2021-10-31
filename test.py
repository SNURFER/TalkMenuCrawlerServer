import selenium, os, shutil, time, pandas, json, datetime
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.options import Options


filePath = os.getcwd() + '/downloads'

def init():

    #download path setting
    option = Options()
    option.add_experimental_option('prefs', {'download.default_directory' : filePath})
    option.add_argument('headless')
    #option.add_argument('--no-sandbox')
    option.add_argument('--window-size=1920x1080')
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

def modifiedEndIdx(menuSheet, menuIdx, totalRow):
    retVal = totalRow
    for row in menuSheet.itertuples():
        if (pandas.isnull(row[7]) and pandas.isnull(row[1]) and pandas.isnull(row[2]) and
         pandas.isnull(row[3]) and pandas.isnull(row[4]) and pandas.isnull(row[5]) and 
         pandas.isnull(row[6]) and row.Index > menuIdx[-1]):
            retVal = row.Index
            break
    return retVal

def parseXLSX(filePath):
    #parse xlsx with pandas 
    menuSheet = pandas.read_excel(filePath, sheet_name=0, engine='openpyxl')

    totalRow = menuSheet.shape[0] - 1

    bldIdx = []
    menuIdx = []

    for row in menuSheet.itertuples():
        if (pandas.isnull(row[1]) == False):
            bldIdx.append(row[0])
        if (pandas.isnull(row[2]) == False):
            menuIdx.append(row[0])
            
    # modifiedEndIdx for bugfix 
    lastIdx = modifiedEndIdx(menuSheet, menuIdx, totalRow)

    # mon tue wed thu fri
    # breakfast lunch dinner
    menuTable = [[0 for i in range(3)] for j in range(5)]
    for i in range(0, 5): 
        bStr = ""
        lStr = "" 
        dStr = "" 
        for row in menuSheet.itertuples():
            #error handling 
            if (row.Index > lastIdx):
                break

            #breakfast
            if (bldIdx[1] <= row[0] and row[0] < bldIdx[2] and pandas.isnull(row[i + 3]) == False):
                if (row[0] in menuIdx):
                    bStr += '\n' + row[2] + '\n'
                bStr += row[i + 3] + '\n'
            #lunch
            if (bldIdx[2] <= row[0] and row[0] < bldIdx[3] and pandas.isnull(row[i + 3]) == False):
                if (row[0] in menuIdx):
                    lStr += '\n' + row[2] + '\n'
                lStr += row[i + 3] + '\n'
            #dinner
            if (bldIdx[3] <= row[0] and row[0] < totalRow and pandas.isnull(row[i + 3]) == False):
                if (row[0] in menuIdx):
                    dStr += '\n' + row[2] + '\n'
                dStr += row[i + 3] + '\n'

        menuTable[i][0] = bStr
        menuTable[i][1] = lStr
        menuTable[i][2] = dStr

    dt = datetime.datetime.now()
    todayBreakfast = ''
    todayLunch = '' 
    todayDinner = ''
    if (dt.strftime('%A') != 'Saturday' and dt.strftime('%A') != 'Sunday'):
        weekday = datetime.datetime.today().weekday()
        todayBreakfast = menuTable[weekday][0]
        todayLunch = menuTable[weekday][1]
        todayDinner = menuTable[weekday][2]
 
    menuJson = {
        "monday" : { 
            "breakfast" : menuTable[0][0],    
            "lunch" : menuTable[0][1],    
            "dinner" : menuTable[0][2],    
        }, 
        "tuesday" : {
            "breakfast" : menuTable[1][0],    
            "lunch" : menuTable[1][1],    
            "dinner" : menuTable[1][2],   
        },
        "wednesday" : {
            "breakfast" : menuTable[2][0],   
            "lunch" : menuTable[2][1],   
            "dinner" : menuTable[2][2],  
        },
        "thursday" : {
            "breakfast" : menuTable[3][0],  
            "lunch" : menuTable[3][1],    
            "dinner" : menuTable[3][2],   
        },
        "friday" : {
            "breakfast" : menuTable[4][0],   
            "lunch" : menuTable[4][1],   
            "dinner" : menuTable[4][2],    
        },
        "today" : {
            "breakfast" : todayBreakfast,   
            "lunch" : todayLunch,   
            "dinner" : todayDinner,    
        }
    }

    with open("menu.json", "w") as menu:
        json.dump(menuJson, menu)


if __name__ == '__main__':
    driver = init()
    downloadPath = navigateAndDownload(driver)
    parseXLSX(downloadPath)
    driver.quit()
