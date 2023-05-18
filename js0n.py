# -*- coding: utf-8 -*-
import os
import time
import json
from collections import OrderedDict
import threading

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # ssl有关
# 定义HTTP请求头
headers = OrderedDict()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
headers['Referer'] = 'https://www.miyoushe.com/'
headers['Connection'] = 'close'


# 加载json文件
with open('output.json', 'r', encoding='utf-8') as file:
    # data = json.load(file)
    data = file.read()
# print(type(data))
json_dict = json.loads(data)

# 获取相关信息
title = json_dict['data']['post']['post']['subject']
post_id = json_dict['data']['post']['post']['post_id']
images_list = json_dict['data']['post']['post']['images']
prev_post_id = json_dict['data']['post']['collection']['prev_post_id']
print(f'post标题是:{title}')
print(f'post_id是:{post_id}')
# print(images_list)
print(f'前一个post_id是:{prev_post_id}')

# =============== Another way get images. ==================
# test = json_dict['data']['post']['post']['content']
# test_dict = json.loads(test)
# print(test_dict['imgs'])
# print(type(test_dict))
# ==========================================================

# 指定保存目录
save_dir = title
# 确保保存目录存在
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def download_image(url):
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        # 从URL中提取文件名
        file_name = url.split('/')[-1]

        # 拼接保存路径
        save_path = os.path.join(save_dir,file_name)

        # 保存响应内容到文件
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f'已下载并保存文件: {save_path}')
    else:
        print(f'无法下载文件: {url}')
    time.sleep(1)

# 创建多个线程并发下载图片
threads = []
for url in images_list:
    thread = threading.Thread(target=download_image, args=(url,))
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

print('多线程下载结束.')