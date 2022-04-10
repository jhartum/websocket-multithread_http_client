import threading
import time

import requests

from config import config


def build_range(value, limit: int = 1024):
    if limit > value:
        return [f'0-{value}']

    lst = []
    x = value

    lst.append(f'{x - limit}-{x}')

    for i in range(int(value / limit)):
        x -= limit
        y = x - limit

        if y > 0:
            lst.append(f'{y}-{x}')
        elif y < 0:
            lst.append(f'{0}-{x}')
    lst.reverse()
    return lst


class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """

    def __init__(self, url, byte_range):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byte_range
        self.req = None

    def get_file_data(self):
        return requests.get(self.__url, stream=True, headers={'Range': f'bytes={self.__byteRange}'}).raw.read()


def download(size_in_bytes: int, link=None, threads: int = config['thread_count'],
             bytes_limit: int = config['limit']):
    start_time = time.time()
    if not link:
        print("Please Enter some url to begin download.")
        return

    file_name = link.split('/')[-1]
    print(f"{size_in_bytes} bytes to download.")
    if not size_in_bytes:
        print("Size cannot be determined.")
        return

    data_list = []
    bytes_range = build_range(int(size_in_bytes), bytes_limit)

    if len(bytes_range) < threads:
        for idx in range(len(bytes_range)):
            byte_range = bytes_range[idx]
            buf_thread = SplitBufferThreads(link, byte_range)
            buf_thread.start()
            buf_thread.join()
            content = buf_thread.get_file_data()
            data_list.append(content)
    elif len(bytes_range) >= threads:
        for idx in range(threads):
            byte_range = bytes_range[idx]
            buf_thread = SplitBufferThreads(link, byte_range)
            buf_thread.start()
            buf_thread.join()
            content = buf_thread.get_file_data()
            data_list.append(content)
    else:
        raise NotImplemented('Something went wrong with range bytes')

    if data_list:
        print(f"--- {str(time.time() - start_time)} seconds ---")
        print(f"All bytes {len(data_list)}")
        with open(f'files/{file_name}', 'wb') as fh:
            for i in data_list:
                fh.write(i)
        print("Finished Writing file %s" % file_name)
