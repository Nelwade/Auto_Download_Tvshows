from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen

from win10toast import ToastNotifier

import chromedriver_autoinstaller
import geckodriver_autoinstaller
import time
import pyautogui
import pydirectinput

notification = ToastNotifier() # creates window notification

def launch_firefoxdriver():
# For Firefox browser
# Firefox does not have download restricitions in headless mode

    # geckodriver_autoinstaller.install() # for autoinstalling geckodriver
    options = Options()
    options.headless = True
    driver = Firefox(
        executable_path = 'D:\\Python projects\\Auto_Download_Tvshows\\webdrivers\\geckodriver',
        options=options
        )
    # drive =webdriver.Firefox()

    driver.implicitly_wait(10)
    return driver

def launch_chromedriver():
    # For Chrome browser

    chromedriver_autoinstaller.install() #automatically installs chromedriver and puts it in the path
    options = webdriver.ChromeOptions()

    # sets the chrome user profile you want to use. This is set to the default profile. Change the path to reflect your preferences
    # or remove the code to let selenium pick a guest account
    options.add_argument(
        "--user-data-dir=C:\\Users\\Stewie\\AppData\\Local\\Google\\Chrome\\User Data"
        )
    # options.headless = True # setting headless mode
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument('--disable-gpu')
    # Prevents chrome from closing itself after execution of commands
    # options.add_experimental_option("detach", True)

    # load the chrome driver. Choose the path where the chromedriver/geckodriver is located.
    # driver = webdriver.Chrome(
    #     executable_path='webdrivers/chromedriver.exe',
    #     chrome_options=options
    #     )


    driver = webdriver.Chrome(chrome_options=options) 
    
    return driver

driver = launch_firefoxdriver()
driver.implicitly_wait(20)
#parent window. Will be useful when closing pop ups
parent_window = driver.current_window_handle 

#driver.maximize_window()

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

def magnet(eps):
    """
    This function extracts and returns the magnet link for a selected download as a string

    """
    magnet = eps.find('span', class_= 'item-icons')
    magnet = magnet.a['href']
    return str(magnet)

def download_torrent_file(magnet_link):
    """
    This function converts the magnet link into a .torrent file that is downloaded
    and automatically loaded by utorrent 
    
    """
    #driver.get("http://magnet2torrent.com/")
    driver.get('https://anonymiz.com/magnet2torrent/')
    # search_box = driver.find_element_by_id('input_box')

    time.sleep(1)

    search_box = driver.find_element_by_id('magnet')
    search_box.send_keys(magnet_link)

    # time.sleep(5)

    driver.find_element_by_id('submit').click()
    
    close_pop_upwindows()
    
    time.sleep(3)

    driver.implicitly_wait(10)
    
    # torrent_link = driver.find_element_by_xpath(
    #     '/html/body/div[2]/div/div/div[1]/div[4]/div/div/div/div/a[1]'
    #     )
    torrent_link = driver.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[1]/div[4]/div/div/div/div/a[3]'  
    )  
    # /html/body/div[2]/div/div/div[1]/div[4]/div/div/div/div/a[3]
    
    torrent_link.click()
    
    download_link = driver.find_element_by_id("torrent-operation-link")
    
    download_link.click()
    print("Torrent file downloaded")
    
    notification.show_toast("Autodownload", "Torrent file downloaded", duration = 3)
    

# enable_download(driver)
# torrent_file("magnet:?xt=urn:btih:59223897F6433166CC6C906ACD13F17722B7E81B&dn=Simple+Plan+-+Harder+Than+It+Looks+%282022%29+Mp3+320kbps+%5BPMEDIA%5D+%E2%AD%90%EF%B8%8F&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fretracker.lanta-net.ru%3A2710%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentor.org%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fipv6.tracker.harry.lu%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.open-internet.nl%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.si%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Fdenis.stalker.upeer.me%3A6969%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce")
# driver.close()
# driver.quit()
# notification.show_toast("Auto", "Chrome Closing", duration = 5)

def open_torrent_app():
    """
    This function opens the torrent app by clicking the 'open torrent' prompt 
    that pops up when magnet link is opened

    Used in non-headless mode
    
    """
    x, y = pyautogui.locateCenterOnScreen('utorrent_button.png', confidence=0.9)
    time.sleep(5)
    pydirectinput.click(x, y)
    #print("clicked on U_torrent button")

def download(resolution):
    """ 
    This function opens the magnet link and and the torrent app after choosing a specific download
    
    """
    magnet_link = ''
    for eps in resolution[0]:
        name = eps.text
        #print(name)
        if "HEVC" in name: # additional filters
            if 'jajaja' in name: # preferred name of torrent uploader
                magnet_link = magnet(eps)
                break
    
    # if the above conditions are not met, this downloads the first element on the list of downloads
    if magnet_link == '': 
        magnet_link = magnet(resolution[0][0])

    download_torrent_file(magnet_link)
    


def search_and_download(search): 
    """
    This function opens the download site, searches the series name and episode, 
    and opens the utorrent app to download it
    
    """
    driver.get("https://thepiratebay.org/index.html")
    torrent = driver.find_elements_by_name("q")[1] # There were more than one search elements named q. The second one was the pirate search

    # perform search for torrent
    torrent.send_keys(search)
    #torrent.send_keys(Keys.ENTER)
    torrent.submit()

    time.sleep(1)

    resolution = select_res('1080p') # selects 1080p resolution
    
    if  resolution[1]!= 0: # if there are results after applying 1080p resolution
        download(resolution)

    else: # if there are no results for 1080p, selects 720p. If there is no 720p you are better off not dowloading it.
        print("1080p Resolution not found. Trying 720p resolution")
        resolution = select_res('720p')
        download(resolution)

def close_browser(): # closes the browser
    driver.close()
    driver.quit()
    notification.show_toast("Autodownload", "Browser Closed", duration = 5)