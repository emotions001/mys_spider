# -*- coding: utf-8 -*-
import requests
import urllib3
from collections import OrderedDict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = OrderedDict()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
headers['Referer'] = 'https://www.miyoushe.com/'
headers['Connection'] = 'close'
proxies = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080"
}
url = "https://bbs-api.miyoushe.com/post/wapi/getPostFull?&post_id=39429516"
response = requests.get(url, verify=False, proxies=proxies, headers=headers)
print(response.text)

if response.status_code == 200:
    with open('output.json', 'w') as file:
        file.write(response.text)
        print('Write out file Seccess!')
else:
    print('Request Error!')