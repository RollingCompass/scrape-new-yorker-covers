# coding: utf-8

import bs4
import requests
import os
import urllib

base_url = 'http://www.coverbrowser.com/covers/new-yorker/'
var_url = 'http://www.coverbrowser.com/covers/new-yorker/'
os.makedirs('NY_covers', exist_ok=True)
page_num = 1
img_num = 1

while not var_url.endswith('75'):
    just_started = True
    # make new folder for image group
    current_folder = 'NY_covers/' + str((page_num - 1) * 50)
    os.mkdir(current_folder)
    # download the page
    print('Downloading page {}...'.format(var_url))
    res = requests.get( var_url)
    res.raise_for_status()
    
    newYorkSoup = bs4.BeautifulSoup(res.text, "lxml")
    # DEBUG: print(newYorkSoup.prettify())
    while img_num % 50 or just_started:
        just_started = False
        # find url of image
        imageElem = newYorkSoup.select('#img' + str(img_num))
        if imageElem == []:
            print( 'Could not find cover image.')
        else:
            print( 'Found something.')
            imageUrl = 'http://www.coverbrowser.com' + imageElem[0].get('src')
            print('Downloading image {}...'.format(imageUrl))
            res = requests.get( imageUrl)
            res.raise_for_status()
        # save the image to ./NY_covers.
            imageFile = open(os.path.join( current_folder, os.path.basename(imageUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        # repeat for next image
        img_num += 1
        # DEBUG: print(img_num)
    # determine the next url to take
    page_num += 1
    var_url = base_url + str(page_num)
print('Done.')
