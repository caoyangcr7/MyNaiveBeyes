# multithread to grab the data from severals websites

import datetime
import MySQLdb
import urllib
from bs4 import BeautifulSoup
import Queue
import threading


home_url1 = 'file:///home/yang/Desktop/specific_data.html'
home_url2 = 'file:///home/yang/Desktop/patient_data.html'
home_url3 = 'file:///home/yang/Desktop/doctors_info.html'
home_urls = [home_url1, home_url2,home_url3]

queue_url = Queue.Queue()   # store the url
queue_html = Queue.Queue()  # store the html of url


class Threadurl(threading.Thread):  # threading.thread is the parent
    """docstring for Threadurl"""

    def __init__(self, queue_url, queue_html):
        threading.Thread.__init__(self)
        self.queue_url = queue_url
        self.queue_html = queue_html

    def run(self):
        while True:
            host = self.queue_url.get()
            html = urllib.urlopen(host)
            self.queue_html.put(html)
            self.queue_url.task_done()


class data_thread(threading.Thread):

    def __init__(self, queue_html):
        threading.Thread.__init__(self)
        self.queue_html = queue_html

    def run(self):
        while True:
            html = self.queue_html.get()
            soup = BeautifulSoup(html, "html5lib", from_encoding='UTF-8')
            data = soup.find_all('td')
            print data[0]
            self.queue_html.task_done()

def main():
    for url in home_urls:
        queue_url.put(url)
    for i in range(3):
        t = Threadurl(queue_url, queue_html)
        t.setDaemon(True)
        t.start()
    for i in range(3):
        dt = data_thread(queue_html)
        dt.setDaemon(True)
        dt.start()
    queue_url.join()  #block the thread,when queue_url is empty,execute the next code
    queue_html.join()


# def operate_database():
#         conn = MySQLdb.connect("192.168.0.119", "root",
#                            "root", "cloud_data", charset="utf8")
#         cursor = conn.cursor()

if __name__ == "__main__":
        start = datetime.datetime.now().replace(microsecond=0)
        main()
        end = datetime.datetime.now().replace(microsecond=0)
        print('--------------------------------------')
        print('running time is {}'.format(end - start))
