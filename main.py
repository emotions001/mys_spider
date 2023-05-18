"""
@ author:VIVA
@ time:2023/5/18 21:24
@ file:main
"""
import os
import time
import json
from collections import OrderedDict

import requests
import urllib3


begin_post_id = input('输入一个post_id:\n>')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = OrderedDict()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
headers['Referer'] = 'https://www.miyoushe.com/'
headers['Connection'] = 'close'

def get_info(begin_post_id):
    url = "https://bbs-api.miyoushe.com/post/wapi/getPostFull?&post_id=" + begin_post_id
    response = requests.get(url, verify=False, headers=headers)
    # print(response.text)
    js0n_info = response.text
    return js0n_info


def save_image(js0n_get):
    data = js0n_get
    json_dict = json.loads(data)
    title = json_dict['data']['post']['post']['subject']
    post_id = json_dict['data']['post']['post']['post_id']
    images_list = json_dict['data']['post']['post']['images']
    prev_post_id = json_dict['data']['post']['collection']['prev_post_id']
    print(f'post标题是:{title}')
    print(f'post_id是:{post_id}')
    # print(images_list)
    print(f'前一个post_id是:{prev_post_id}')

    save_dir = title
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for url in images_list:
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == 200:
            # 从URL中提取文件名
            file_name = url.split('/')[-1]

            # 拼接保存路径
            save_path = os.path.join(save_dir, file_name)

            # 保存响应内容到文件
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f'已下载并保存文件: {save_path}')
        else:
            print(f'无法下载文件: {url}')
        time.sleep(1)


if __name__ == '__main__':
    result = get_info(begin_post_id)
    save_image(result)
    # print(result)










