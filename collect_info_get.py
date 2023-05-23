# -*- coding: utf-8 -*-
import json

import requests
import urllib3
from collections import OrderedDict

# 从json文件中获取信息——读取
with open('output.json', 'r', encoding='utf-8') as file:
    data = file.read()
    json_dict = json.loads(data)

# 获取相关信息
collect_id = json_dict['data']['post']['collection']['collection_id']

print(f'该post合集id是:{collect_id}')

# 开始构造请求体
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = OrderedDict()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
headers['Referer'] = 'https://www.miyoushe.com/'
headers['Connection'] = 'close'

url = 'https://bbs-api.miyoushe.com/post/wapi/getPostFullInCollection?collection_id='+ collect_id +'&gids=2&order_type=1'

response = requests.get(url, verify=False, headers=headers)
print(response.text)

if response.status_code == 200:
    with open('collect.json', 'w') as file:
        file.write(response.text)
        print('Write success!')
else:
    print('Request Error!')
