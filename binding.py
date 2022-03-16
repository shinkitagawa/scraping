# -*- coding: utf-8 -*-
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
# import chromedriver_binary

########################################

# scraping.pyを読み込み実行

########################################
#<<<<<<<<<<<< 変数・関数定義 >>>>>>>>>>>>#

path = 'download/' + title + '/'
vol_total_count = 0

def findMedianSize(image_urls):
    sizes = {"height":[],"width":[]}
    for a in image_urls:
        read_img = cv2.imread(a)
        height, width = read_img.shape[:2]
        sizes["height"].append(math.floor(height))
        sizes["width"].append(math.floor(width))

    return (int(statistics.median(sizes['height'])), int(statistics.median(sizes['width'])))


####################################
#<<<<<<<<<<<< スクリプト >>>>>>>>>>>>#

#ディレクトリから画像を全て読み込む
vol_total_count = len(glob.glob(path + 'raw_images/*'))
for vol in range(vol_total_count):
    print('[ORGANIZING]' + title + '  Vol.' + str(vol + 1))
    if len(glob.glob(path + 'raw_images/' + str(vol+1) + '/*')) > 1:
        ims_address = glob.glob(path + 'raw_images/' + str(vol+1) + '/*')
        ims_address = sorted(ims_address, key=lambda s: int(re.findall(r'\d+', s)[1]), reverse=True)

        #見開きページの作成
        tmp_hconcat_list = []
        image_height, image_width = findMedianSize(ims_address)
        while len(ims_address) > 1:
            ims_sizes = [[0,0],[0,0]]
            img_adress_1 = ims_address.pop()
            img_adress_2 = ims_address.pop()
            img_1 = cv2.imread(img_adress_1)
            img_2 = cv2.imread(img_adress_2)
            ims_sizes[0][0], ims_sizes[0][1]= img_1.shape[:2]
            ims_sizes[1][0], ims_sizes[1][1] = img_2.shape[:2]
            if ims_sizes[0][0] > ims_sizes[0][1] and ims_sizes[1][0] > ims_sizes[1][1]:
                img_1 = cv2.resize(img_1,(image_width, image_height))
                img_2 = cv2.resize(img_2,(image_width, image_height))
                hconcat_img = cv2.hconcat([img_2,img_1])
                resized_hconcat_img = cv2.resize(hconcat_img,(image_width*2, image_height))
                tmp_hconcat_list.append(resized_hconcat_img)
            elif ims_sizes[0][0] < ims_sizes[0][1] and ims_sizes[1][0] < ims_sizes[1][1]:
                resized_hconcat_img_1 = cv2.resize(img_1,(image_width*2, image_height))
                resized_hconcat_img_2 = cv2.resize(img_2,(image_width*2, image_height))
                tmp_hconcat_list.append(resized_hconcat_img_1)
                tmp_hconcat_list.append(resized_hconcat_img_2)
            elif ims_sizes[0][0] < ims_sizes[0][1]:
                resized_hconcat_img_1 = cv2.resize(img_1,(image_width*2, image_height))
                tmp_hconcat_list.append(resized_hconcat_img_1)
                ims_address.append(img_adress_2)
            elif ims_sizes[1][0] < ims_sizes[1][1]:
                resized_hconcat_img_2 = cv2.resize(img_2,(image_width*2, image_height))
                tmp_hconcat_list.append(resized_hconcat_img_2)
                ims_address.append(img_adress_1)

        hconcat_list = []
        #見開きページに余白を追加
        for index, hconcat_img in enumerate(tmp_hconcat_list):
            size = image_width*2
            new_img = cv2.resize(np.zeros((1, 1, 3), np.uint8), (size, size-80))

            start = int((size - image_height) / 2)
            fin = int((size + image_height) / 2)
            new_img[start:fin, :] = hconcat_img
            hconcat_list.append(new_img)
            print('[' + str(index + 1) + '/' + str(len(tmp_hconcat_list)) + ']' + '[CREATE MARGIN]' + img_adress_1 + '  &&  ' + img_adress_2)

        print('[FINISHING]' + title + '  Vol.' + str(vol + 1))
        #１巻を４等分にする
        lists = []
        if len(hconcat_list) >= 4:
            lists = [hconcat_list[idx:idx + -(-len(hconcat_list) // 4)] for idx in range(0,len(hconcat_list), -(-len(hconcat_list) // 4))]
        else:
            lists = hconcat_list

        #画像を抽出
        print('[SAVING]' + title + '  Vol.' + str(vol + 1))
        for number,list in enumerate(lists):
            img_vconcat = cv2.vconcat(list)
            cv2.imwrite(path + 'vol_{}-{}.jpg'.format(vol+1,number+1), img_vconcat,[cv2.IMWRITE_JPEG_QUALITY, 50])
    else:
        print('skipped Vol.' + str(vol+1))

print('---------------------------------------------')
print('---------------------------------------------')
print(str(vol_total_count) + 'volumes Successfully downloaded')
print('---------------------------------------------')
print('---------------------------------------------')
