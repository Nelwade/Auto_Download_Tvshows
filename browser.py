from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen

from win10toast import ToastNotifier

import time
import pyautogui
import pydirectinput

notification = ToastNotifier() # creates window notification
# For Firefox- Unindent to use
    # options = Options()
    # driver = Firefox(executable_path = 'C:/geckodriver', options=options)

options = webdriver.ChromeOptions()

# sets the chrome user profile you want to use. This is set to the default profile. Change the path to reflect your preferences
# or remove the code to let selenium pick a guest account
options.add_argument(
    "--user-data-dir=C:\\Users\\Stewie\\AppData\\Local\\Google\\Chrome\\User Data"
    )

# Prevents chrome from closing itself after execution of commands
# options.add_experimental_option("detach", True)

# load the chrome driver. Choose the path where the chromedriver/geckodriver is located.
driver = webdriver.Chrome(
    executable_path='webdrivers/chromedriver',
    chrome_options=options
    ) 
driver.implicitly_wait(0.5)

#parent window. Will be useful when closing pop ups
parent_window = driver.current_window_handle 

def close_pop_upwindows():
    """
    This function closes any pop up windows due to ads
    """

    uselessWindows = driver.window_handles # pop up windows that may occur
    if len(uselessWindows) > 1:
        for window in uselessWindows:
            if window != parent_window:
                driver.switch_to.window(window)
                driver.close()
        time.sleep(2)
        driver.switch_to.window(parent_window)


def select_res(res):
    """
    This function selects a desired resolution by checking a box
    Returns a list of all results after filtering and the length of the list

    """
     # resolution = driver.find_element_by_xpath("//input[@id='f_1080p']")
    #print("Applying {} filter".format(res))
    driver.find_element_by_id('f_'+ res).click() # applying resolution filter

    close_pop_upwindows()
    
    # Check if resolution checkbox is selected, if not it tries again until selected
    while not driver.find_element_by_id('f_' + res).is_selected():
        driver.find_element_by_id('f_' + res).click()
        time.sleep(5)

    time.sleep(5)
    html = driver.page_source   # gets page source after selection of filter
    soup = BeautifulSoup(html, 'html.parser')
    filtered = soup.find_all('li', id= 'st', style ='') # Provides a list of filtered results
    return [filtered, len(filtered)]

def magnet_link(eps):
    """
    This function extracts and returns the magnet link for a selected download as a string

    """
    magnet = eps.find('span', class_= 'item-icons')
    magnet = magnet.a['href']
    return str(magnet)

def open_torrent_app():
    """
    This function opens the torrent app by clicking the 'open torrent' prompt 
    that pops up when magnet link is opened
    
    """
    x, y = pyautogui.locateCenterOnScreen('utorrent_button.png', confidence=0.9)
    time.sleep(5)
    pydirectinput.click(x, y)
    #print("clicked on U_torrent button")

def download(resolution):
    """ 
    This function opens the magnet link and and the torrent app after choosing a specific download
    
    """
    download_link = ''
    for eps in resolution[0]:
        name = eps.text
        #print(name)
        if "HEVC" in name: # additional filters
            if 'jajaja' in name: # preferred name of torrent uploader
                download_link = magnet_link(eps)
                break
    
    # if the above conditions are not met, this downloads the first element on the list of downloads
    if download_link == '': 
        download_link = magnet_link(resolution[0][0])

    driver.get(download_link) # opens magnet link
    time.sleep(5)
    close_pop_upwindows() # closes ads
    open_torrent_app ()
    print("Download Initiated.......\n\n\n")
    notification.show_toast("AutoDownload", "uTorrent Opened for Download. Please Accept or Deny Download", duration = 60)


def search_and_download(search): 
    """
    This function opens the download site, searches the series name and episode, 
    and opens the utorrent app to download it
    
    """
    driver.get("https://thepiratebay.org/index.html")
    torrent = driver.find_elements_by_name("q")[1] # There were more than one search elements named q. The second one was the pirate search
    driver.implicitly_wait(10)

    # perform search for torrent
    torrent.send_keys(search)
    driver.implicitly_wait(1)
    #torrent.send_keys(Keys.ENTER)
    torrent.submit()

    time.sleep(10)

    resolution = select_res('1080p') # selects 1080p resolution
    
    if  resolution[1]!= 0: # if there are results after applying 1080p resolution
        download(resolution)

    else: # if there are no results for 1080p, selects 720p. If there is no 720p you are better off not dowloading it.
        print("1080p Resolution not found. Trying 720p resolution")
        resolution = select_res('720p')
        download(resolution)

def close_browser(): # closes the browser
    time.sleep(5)
    driver.close()