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
import os
import pyautogui
import pydirectinput
import glob


# options = Options()
# driver = Firefox(executable_path = 'C:/geckodriver', options=options)       #load firefox



options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\Stewie\\AppData\\Local\\Google\\Chrome\\User Data")
#options.add_experimental_option('excludeSwitches', ['disable-default apps'])
#options.add_argument('--disable-default-apps')
# options.add_experimental_option(
#     'excludeSwitches',
#     ['disable-sync', 'disable-default apps']) 
# options.add_argument('--enable-sync')
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

    time.sleep(10)

    # resolution = driver.find_element_by_xpath("//input[@id='f_1080p']")
    print("Apllying 1080 filter")
    driver.find_element_by_id("f_1080p").click() # applying resolution filter
    #driver.find_element_by_id("f_1080p").click()

    #close_pop_upwindows()

    while not driver.find_element_by_id('f_1080p').is_selected():
        driver.find_element_by_id("f_1080p").click()
        time.sleep(5)

    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #filtered_1080 = soup.find_all('li', id= 'st')
    filtered_1080 = soup.find_all('li', id= 'st', style ='')
    
    if len(filtered_1080) != 0:
        

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

                    # #driver.get("http://magnet2torrent.com/")
                    # driver.get('https://anonymiz.com/magnet2torrent/')
                    # # search_box = driver.find_element_by_id('input_box')
                    # search_box = driver.find_element_by_id('magnet')
                    # search_box.send_keys(magnet)

                    # time.sleep(5)

                    # driver.find_element_by_id('submit').click()
                    # print("submitted")
                    # driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div[4]/div/div/div/div/a[1]').click()
                    
                    #driver.implicitly_wait(3)
                    # search_box.send_keys(Keys.ENTER)
                    #search_box.submit()

                    # downloads = glob.glob('C:\\Users\\Stewie\\Downloads' + '\Ztorrent')
                    # print(downloads)

                    
                    #close_pop_upwindows()
                    time.sleep(5)
                    x, y = pyautogui.locateCenterOnScreen('utorrent_button.png', confidence=0.9)
                    time.sleep(5)
                    pydirectinput.click(x, y)
                    print("clicked on U_torrent button")
                    #pyautogui.click('utorrent_button.png')
                    
                    # WebDriverWait(driver, 50).until(EC.alert_is_present())

                    # alert = driver.switch_to.alert()
                    # alert = Alert(driver)
                    # #time.sleep(5)
                    # #print(alert.text)
                    # alert.accept()

                    break
                else: 
                    continue
            else: continue
    else:
        print("1080 not available")
        time.sleep(5)
        print("Removing 1080 filter")
        driver.find_element_by_id("f_720p").click() # remove 1080 filter
        #driver.find_element_by_id("f_1080p").click()
        #driver.find_element_by_id("f_720p").click()

        time.sleep(10)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        filtered = soup.find_all('li', id= 'st', style =None)

        time.sleep(5)

        print(len(filtered))
        for eps in filtered:
            name = eps.text
            print(name)
            if "HEVC" in name:
                if 'jajaja' in name:
                    print(name)
                    magnet = eps.find('span', class_= 'item-icons')
                    magnet = magnet.a['href']
                    #print(magnet)
                
                    driver.get(str(magnet)) # selects the magnet icon to download torrent
                    # close_pop_upwindows()
                    time.sleep(5)
                    x, y = pyautogui.locateCenterOnScreen('utorrent_button.png', confidence=0.9)
                    time.sleep(5)
                    pydirectinput.click(x, y)
                    print("clicked on u_torrent button")
                    break
                else: 
                    break
            else: continue
    
    # time.sleep(10)
    # driver.close()
        

# torrent.send_keys(Keys.ENTER)



