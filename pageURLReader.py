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
from .functions import imgProcessor


def returnIndivisualPageUrlArray():
    #空の配列を生成
    urls = []
    page_urls = []
    page_urls.append(page_url)
    number = 2
    #漫画のURLを含んだウェブページを全て取得する
    not_last_page = True
    while not_last_page == True:
        res = requests.get(page_url + "page" + str(number) + "/")
        if res.status_code != 404:
            page_urls.append(page_url + "page" + str(number) + "/")
            number = number + 1
        else:
            not_last_page = False

    #１冊ごとのURLを取得する
    for _page_url in page_urls:
        res = urllib.request.urlopen(_page_url)
        soup = BeautifulSoup(res, "html.parser")
        elems = soup.find_all(class_='entry-header')
        #titleを含んだ巻名であれば各要素に対してhref属性を取得
        for elem in elems:
            if title in elem.get_text():
                url = elem.find('a').get("href")
                urls.append(url)
                print(elem.get_text())
    return urls
