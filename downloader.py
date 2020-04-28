#!/usr/bin/python3

import sys
import requests
import argparse

from bs4 import BeautifulSoup as BS
from colorama import Fore, init

def main():
    print()
    init() # enable colorama on windows xD
    parser = argparse.ArgumentParser(description='Mix.Tj video downloader')
    parser.add_argument("url", type=str, help="Url of video on Mix.TJ")
    parser.add_argument("--filename", type=str, default='None', help='Filename (for save video)')
    parser.add_argument("--dir", type=str, default="", help='Directory to save file...')
    names = parser.parse_args()
    
    if not names.url.startswith("http://mix.tj/video"):
        print(Fore.LIGHTRED_EX + "Invalid url")
        return
    
    try:
        r = requests.get(names.url)

    except:
        print(Fore.LIGHTRED_EX + "Invalid url or bad connection...")
        return 

    if r.status_code != 200:
       print(Fore.LIGHTRED_EX + "Status code is not 200, bad connection or invalid url, you can try again xD")
       return

    soup = BS(r.content, 'html.parser')
    
    if names.filename == 'None':
        video_title = soup.select("title")[0].text.split("|")[0]
        filename = video_title
    else:
        filename = names.filename

    filename += '.mp4'
    
    if soup.video:
        link = soup.video.source.attrs['src']
    else:
        print(Fore.LIGHTRED_EX + "Video not found, check your link...")
        return 

    print(Fore.LIGHTGREEN_EX + "You video found! as " + video_title)
    print(Fore.LIGHTGREEN_EX + "Video size is " + soup.select(".fa-server")[0].next)
    print(Fore.LIGHTYELLOW_EX + "Loading " + filename)
    video = requests.get(link)
    
    if video.status_code != 200:
        print(Fore.LIGHTRED_EX + "Status code is not 200, sorry...")
        return

    if names.dir:
        filename = names.dir + '/' + filename

    f = open(filename, 'wb')
    print("Saving to file...")
    f.write(video.content)
    f.close()
    print(Fore.LIGHTYELLOW_EX + "Closing file")
    print(Fore.LIGHTGREEN_EX + "Video Succefully downloaded to -> \"" + filename + '"')

if __name__ == '__main__':
    main()
