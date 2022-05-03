# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:23:09 2022

@author: Owade
"""


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from browser import close_browser, search_and_download
from win10toast import ToastNotifier

import re
import sys
import re
import os
import datetime

notification = ToastNotifier() # creates window notification

def if_in_favourites (tv_show_name):
    os.chdir(r'C:\Users\Stewie\Dropbox\My PC (DESKTOP-57VNQ1O)\Documents\Python projects\Auto_Download_Tvshows')
    with open('Favourite_Tvshows.txt') as file:
        if tv_show_name.lower() in file.read():
            return True
        else:
            return False

def yester_episodes(): # returns all episodes from the previous day and dowloads each of them
    x = Request("https://next-episode.net/recent/",
                headers={'User-Agent': 'Mozilla/5.0'}) # next-episode is a website that shows recent episodes
    x = urlopen(x)
    html = x.read().decode("latin-1")
    soup = BeautifulSoup(html, "html.parser")

    recent_episodes = soup.find_all('span', class_ = "footer") # recent episodes are within <span class = "footer">
    yester_eps = recent_episodes[2] # yesterday's episodes, which are ready to download are in the third span tag

    yester_eps = yester_eps.find_all('div')

    #all_episodes = dict() # All episodes from yesteday, dict will contain name of episode as key, and episode number as value
    for div in yester_eps:

        tv_show_name = div.h3.string

        if if_in_favourites(tv_show_name) == True:

            ep_num = re.search('-\s.*\s-', div.text)
            ep_num = ep_num.group().strip("-").strip()
            ep_num = ep_num.split('x')
            
            season = ep_num[0]
            
            if int(season) < 10:
                season = "S0" + str(season)
            else:
                season = "S" + str(season)

            episode = "E" + str(ep_num[1])
            
            ep_num = season + episode
            episode_name = tv_show_name + " " + ep_num

            print("Downloading {}\n".format(episode_name))
            notification.show_toast("AutoDownload", ("Downloading {}".format(episode_name)), duration = 30)

            
            search_and_download(episode_name) # Downloads the episode by name
            #all_episodes[tv_show_name] = ep_num
        else:
            continue


def exc():
    time = datetime.datetime.now()
    print("\n\n", time, "\n-----------------------------------\n")
    try:
        yester_episodes()
    except:
        print(sys.exc_info())



# Manually creating logs in a selected folder

os.chdir(
    'C:\\Users\\Stewie\\Dropbox\\My PC (DESKTOP-57VNQ1O)\\Documents\\Python projects\\Auto_Download_Tvshows'
    )
if os.path.exists('logs.txt'):
    with open('logs.txt', 'a', encoding="utf-8") as logs:
        sys.stdout = logs
        exc()   
else:
    with open('logs.txt', 'w', encoding="utf-8") as logs:
        sys.stdout = logs
        exc()
        
close_browser()





# with open('pirate.txt', 'w') as next:
# for line in x:
# next.write(line.decode())
