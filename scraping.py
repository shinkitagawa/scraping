import webbrowser
from selenium import webdriver
import io
import urllib.request
import sys
import urllib
from bs4 import BeautifulSoup
from PIL import Image
import time
import os
import pprint
import urllib.error
import cv2
import numpy as np
import glob
import re
import tempfile
import requests
import copy
import math
import shutil
import statistics

from env import *
from . import imgProcessor
from . import pageURLReader
# import chromedriver_binary

########################################
#<<<<<<<<<<<< 変数定義 >>>>>>>>>>>>#

headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0" }
path = 'download/' + title + '/'

path_vol = 0
img_id = 1
vol_total_count = 0


########################################
#<<<<<<<<<<<< 処理　 >>>>>>>>>>>>#

os.makedirs(path + 'raw_images', exist_ok=True)
browser = webdriver.Chrome()
urls = pageURLReader.returnIndivisualPageUrlArray()
urls.reverse()

for index, url in enumerate(urls):
    browser.get(url)
    #画像の属性を全て取得する
    images = browser.find_elements_by_class_name('attachment-large')
    #巻ごとのディレクトリを作成する
    path_vol = index + 1
    os.makedirs(path + 'raw_images/' + str(path_vol), exist_ok=True)

    print('[SCRAPING][' + str(index + 1) + '/' + str(len(urls)) + ']  ' + url)

    for _index, _image in enumerate(images):
        #画像を一枚ずつ読み込む
        img_url = _image.get_attribute('data-src')
        raw_img = imgProcessor.imread_web(img_url)
        #作成した巻ごとのディレクトリに画像を保存する
        dst_path = path + 'raw_images/' + str(path_vol) + '/image_' + str(img_id) + '.jpg'
        cv2.imwrite(dst_path, raw_img)
        img_id = img_id + 1


browser.quit()

print('___________________________')
print('scraping ' + title + 'fin')
print('___________________________')
