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
#<<<<<<<<<<<< 変数定義 >>>>>>>>>>>>#

headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0" }
path = 'download/' + title + '/'

path_vol = 0
img_id = 1
vol_total_count = 0

########################################
#<<<<<<<<<<<< 関数定義 >>>>>>>>>>>>#
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
    return urls

#画像処理を軽くする関数
def imread_web(url):
    # 画像をリクエストする
    res = requests.get(url)
    img = None
    # Tempfileを作成して即読み込む
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img


def find_median(image_urls):
    sizes = {"height":[],"width":[]}
    for a in image_urls:
        read_img = cv2.imread(a)
        height, width = read_img.shape[:2]
        sizes["height"].append(math.floor(height))
        sizes["width"].append(math.floor(width))

    return (int(statistics.median(sizes['height'])), int(statistics.median(sizes['width'])))


########################################
#<<<<<<<<<<<< 処理　 >>>>>>>>>>>>#

#スクレイピング

os.makedirs(path + 'raw_images', exist_ok=True)
browser = webdriver.Chrome()
urls = returnIndivisualPageUrlArray()
urls.reverse()

for index, url in enumerate(urls):
    browser.get(url)
    #画像の属性を全て取得する
    images = browser.find_elements_by_class_name('attachment-large')
    #巻ごとのディレクトリを作成する
    path_vol = index + 1
    os.makedirs(path + 'raw_images/' + str(path_vol), exist_ok=True)

    print('[SCRAPING][' + str(index + 1) + '/' + str(len(urls)) + ']  ' + url)

    for _index, image in enumerate(images):
        #画像を一枚ずつ読み込む
        img_url = image.get_attribute('data-src')
        raw_img = imread_web(img_url)
        #作成した巻ごとのディレクトリに画像を保存する
        dst_path = path + 'raw_images/' + str(path_vol) + '/image_' + str(img_id) + '.jpg'
        cv2.imwrite(dst_path, raw_img)
        img_id = img_id + 1


browser.quit()

print('___________________________')
print('scraping ' + title + 'fin')
print('___________________________')


#バインディング

vol_total_count = len(glob.glob(path + 'raw_images/*'))
for vol in range(vol_total_count):
    print('[ORGANIZING]' + title + '  Vol.' + str(vol + 1))
    if len(glob.glob(path + 'raw_images/' + str(vol+1) + '/*')) > 1:
        ims_address = glob.glob(path + 'raw_images/' + str(vol+1) + '/*')
        ims_address = sorted(ims_address, key=lambda s: int(re.findall(r'\d+', s)[1]), reverse=True)

        #見開きページの作成
        tmp_hconcat_list = []
        image_height, image_width = find_median(ims_address)
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
