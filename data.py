import os
import pathlib
from typing import List, Dict

import requests


def prepare_data(urls: List) -> List[Dict]:
    url_data = []
    headers = {"Range": "bytes=0-1"}

    exist_files = []

    for r, d, f in os.walk(str(pathlib.Path(os.path.abspath(__file__)).parent) + '/files'):
        for files in f:
            exist_files.append(files)

    for url in urls:
        r = requests.get(url)
        url_dict = {}

        url_dict.update({'size': r.headers['Content-Length']})

        if str(url.split("/")[-1]) in exist_files:
            url_dict.update({
                'url': f'file:///{str(pathlib.Path(os.path.abspath(__file__)).parent) + "/files"}',
                'processed': True
            })
        else:
            url_dict.update({'url': url, 'processed': False})

        range_check = requests.get(url, headers=headers)
        code = range_check.status_code
        if code == 206:
            url_dict.update({'ranges': True})

        url_data.append(url_dict)
    return url_data
