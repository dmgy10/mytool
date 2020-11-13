# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:20:05 2019

@author: yuyh2
"""

"""
爬虫
"""
from urllib.request import urlretrieve
import os

class craw:
    @staticmethod
    def urllib_image_download(image_url, image_dir, image_name):
        download_dir = os.path.join('./', image_dir)
        os.makedirs(download_dir, exist_ok = True)
        urlretrieve(image_url, os.path.join(download_dir, image_name + '.png'))