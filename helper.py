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





def findMedianSize(image_urls):
    sizes = {"height":[],"width":[]}
    for a in image_urls:
        read_img = cv2.imread(a)
        height, width = read_img.shape[:2]
        sizes["height"].append(math.floor(height))
        sizes["width"].append(math.floor(width))

    return (int(statistics.median(sizes['height'])), int(statistics.median(sizes['width'])))
