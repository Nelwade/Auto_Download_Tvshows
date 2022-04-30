from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import time


# options = Options()
# driver = Firefox(executable_path = 'C:/geckodriver', options=options)       #load firefox



options = webdriver.ChromeOptions()
#options.add_experimental_option('excludeSwitches', ['disable-default apps'])
#options.add_argument('--disable-default-apps')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path='C:/chromedriver', chrome_options=options) # load the chrome driver
driver.implicitly_wait(0.5)


parent_window = driver.current_window_handle #parent window. Will be useful when closing pop ups

def close_pop_upwindows():
    uselessWindows = driver.window_handles # pop up windows may occur
    if len(uselessWindows) > 1:
        for window in uselessWindows:
            if window != parent_window:
                driver.switch_to.window(window)
                driver.close()
    driver.switch_to.window(parent_window)
            

def download(search): 
    driver.get("https://thepiratebay.org/index.html")
    torrent = driver.find_elements_by_name("q")[1] # There were more than one search elements named q. The second one was the pirate search
    driver.implicitly_wait(10)

    # perform search for torrent
    torrent.send_keys(search)
    driver.implicitly_wait(1)
    #torrent.send_keys(Keys.ENTER)
    torrent.submit()

    time.sleep(5)

    # resolution = driver.find_element_by_xpath("//input[@id='f_1080p']")
    driver.find_element_by_id("f_1080p").click() # applying resolution filter
    time.sleep(5)
    driver.find_element_by_id("f_1080p").click()

    # print(driver.find_element_by_id('f_1080p').is_selected())

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #filtered_1080 = soup.find_all('li', id= 'st')
    filtered_1080 = soup.find_all('li', id= 'st', style ='')

    for eps in filtered_1080:
        name = eps.text
        #print(name)
        if "HEVC" in name:
            if 'jajaja' in name:
                print(name)
                magnet = eps.find('span', class_= 'item-icons')
                magnet = magnet.a['href']
                print(magnet)
                driver.get(str(magnet)) # selects the magnet icon to download torrent

                close_pop_upwindows()
                
                # WebDriverWait(driver, 50).until(EC.alert_is_present())

                # alert = driver.switch_to.alert()
                # alert = Alert(driver)
                # #time.sleep(5)
                # #print(alert.text)
                # alert.accept()

                break
            else: 
                break
        else: continue
    

# torrent.send_keys(Keys.ENTER)



