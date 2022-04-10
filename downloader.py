import threading
import time

import requests

url = "https://i.imgur.com/AHUAvly.jpeg"


# url = 'http://pymotw.com/2/urllib/index.html'
# url = 'http://megaboon.com/common/preview/track/786203.mp3' # size cannot be determined.
# url = 'http://broadcast.lds.org/churchmusic/MP3/1/2/nowords/271.mp3'


def buildRange(value, limit: int = 1024):
    if limit > value:
        return [f'0-{value}']

    lst = []
    x = value

    lst.append(f'{x - limit}-{x}')

    for i in range(int(value / limit)):
        x -= limit
        y = x - limit

        if y > 0:
            a = f'{y}-{x}'
            print('> o', a)
            lst.append(a)
        elif y < 0:
            a = f'{0}-{x}'
            print('< o', a)
            lst.append(a)
    lst.reverse()
    return lst


class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """

    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None

    def getFileData(self):
        y = requests.get(self.__url, stream=True, headers={'Range': f'bytes={self.__byteRange}'}).raw.read()
        return y


def download(size_in_bytes: int, link=None, threads: int = 3, bytes_limit: int = 1024):
    start_time = time.time()
    if not link:
        print("Please Enter some url to begin download.")
        return

    file_name = link.split('/')[-1]
    # size_in_bytes = requests.head(link, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    print(f"{size_in_bytes} bytes to download.")
    if not size_in_bytes:
        print("Size cannot be determined.")
        return

    data_list = []
    bytes_range = buildRange(int(size_in_bytes), bytes_limit)
    print(bytes_range)
    for idx in range(len(bytes_range)):
        byte_range = bytes_range[idx]
        buf_thread = SplitBufferThreads(link, byte_range)
        buf_thread.start()
        buf_thread.join()
        content = buf_thread.getFileData()
        data_list.append(content)

    if data_list:
        print(f"--- {str(time.time() - start_time)} seconds ---")
        print(f"All bytes {len(data_list)}")
        with open(f'files/{file_name}', 'wb') as fh:
            for i in data_list:
                fh.write(i)
        print("Finished Writing file %s" % file_name)
