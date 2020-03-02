import urllib.request
from urllib.error import HTTPError, URLError
from threading import Thread
import socket
import chardet
import logging
# import gzip
# import io


class GetUrlThread(Thread):
    def __init__(self, url):
        self.url = url
        super(GetUrlThread, self).__init__()
        self.alive = ""

    def run(self):
        try:
            # .read() .decode('utf-8', 'ignore')
            response = urllib.request.urlopen(self.url, timeout=10)
        except HTTPError as error:
            logging.error(
                'Data not retrieved because %s\nURL: %s', error, self.url)
        except URLError as error:
            if isinstance(error.reason, socket.timeout):
                logging.error('socket timed out - URL %s', self.url)
            else:
                logging.error(
                    'some other error happened while probing: ' + self.url)
        else:
            logging.info('Access successful.')
            DOWN_RESPONSES = ["Svetainė išjungta",
                              "Website is disabled", "Веб-сайт выключен",
                              "/defaultwebpage.cgi",
                              "been a server misconfiguration",
                              "may have moved to a different server"]
            buffer = response.read()
            # buffer = io.BytesIO(response.read())
            # gziped_file = gzip.GzipFile(fileobj=buffer)
            # decoded = gziped_file.read()
            encoding = chardet.detect(buffer)
            print("encoding: " + encoding['encoding'])
            content = buffer.decode(encoding['encoding'])
            if not any(x in content for x in DOWN_RESPONSES):
                self.alive = self.url
                print(self.url + "  " + str(response.getcode()))
                # print(content)
            else:
                print(self.url + "  " + "-Website turned off by Host-")
