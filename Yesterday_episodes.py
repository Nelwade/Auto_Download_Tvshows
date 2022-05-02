# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:23:09 2022

@author: Stewie
"""

import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import os
import browser

def if_in_favourites (tv_show_name):
    os.chdir(r'C:\Users\Stewie\Dropbox\My PC (DESKTOP-57VNQ1O)\Documents\Python projects\Auto_Download_Tvshows')
    with open('Favourite_Tvshows.txt') as file:
        if tv_show_name.lower() in file.read():
            return True
        else:
            return False

def all_episodes(): # returns all episodes from the previous day that can be downloaded in a dictionary
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
            search = tv_show_name + " " + ep_num
            print("Downloading {}".format(search))
            browser.download(search)
            #all_episodes[tv_show_name] = ep_num
        else:
            continue

all_episodes()
    
    # print(tv_show_name)
    # print(season, " ", episode)
    # print(ep_num)
    # print("\n\n")
    



# with open('pirate.txt', 'w') as next:
# for line in x:
# next.write(line.decode())
