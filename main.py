# -*- coding: utf-8 -*-
import os
import time
import json
from collections import OrderedDict
import threading

import requests
import urllib3

beginning_collect_id = input("请输入一个合集的ID\n>")

# 构造请求头数据
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = OrderedDict()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
headers['Referer'] = 'https://www.miyoushe.com/'
headers['Connection'] = 'close'

# 定义ANSI转义码
ANSI_GREEN = '\033[92m'
ANSI_YELLOW = '\033[93m'
ANSI_END = '\033[0m'

def get_json(beginning_collect_id):
    url = 'https://bbs-api.miyoushe.com/post/wapi/getPostFullInCollection?collection_id=' + beginning_collect_id + '&gids=2&order_type=1'
    response = requests.get(url, verify=False, headers=headers)
    resource = response.text
    if response.status_code == 200:
        print(ANSI_GREEN + 'Get source success' + ANSI_END)
    else:
        print('Request Error!')
    return resource

def save_image(resource_info):
    json_dict = json.loads(resource_info)

    # 开始取出JSON文件信息
    sub_json = json_dict['data']['posts']

    count = 0
    for list in sub_json:
        info = list['post']
        post_id = info['post_id']
        subject = info['subject']
        images = info['images']
        count += 1
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f'post_id:{post_id}')
        print(f'标题是:{subject}')
        print(ANSI_GREEN + f'开始下载第{count}个' + ANSI_END)
        # 构建下载目录
        save_dir = subject
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        def download_image(url):
            response = requests.get(url, verify=False, headers=headers)
            if response.status_code == 200:
                # 获取文件名
                file_name = url.split('/')[-1]
                # 拼接保存路径
                save_path = os.path.join(save_dir, file_name)
                # 保存响应内容到文件
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f'已下载并保存文件: {save_path}')
            else:
                print(f'无法下载文件: {url}')
            time.sleep(0.7)

        # 创建多线程并发下载
        threads = []
        for url in images:
            thread = threading.Thread(target=download_image, args=(url,))
            thread.start()
            threads.append(thread)

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        print(ANSI_YELLOW + '多线程下载结束.' + ANSI_END)


if __name__ == '__main__':
    result = get_json(beginning_collect_id)
    save_image(result)



