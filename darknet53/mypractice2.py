import urllib
from bs4 import BeautifulSoup
import datetime
import MySQLdb


home_url = 'file:///home/yang/Desktop/specific_data.html'

def get_links(article_url):
    html = urllib.urlopen(article_url)
    bsObj = BeautifulSoup(html, "html5lib", from_encoding='UTF-8')
    m_th = bsObj.find_all('th')
    length_title = len(m_th)  # 68
    print(length_title)
    m_td = bsObj.find_all('td')
    print(len(m_td))   # 333954
    print(m_td[0:3])

    title = bsObj.find_all('th')
    title_from_web = []
    for i in range(len(title)):
        title_from_web.append(str(title[i]).split('<th>')[1].split('</th>')[0])
    # print(title_from_web)

    data_from_web = []
    for i in range(len(m_td)):
        data_from_web.append(str(m_td[i]).split('<td>')[1].split('</td>')[0].replace('\xc2\xa0', ''))
        
    new_m_td = [tuple(data_from_web[(length_title * i): (length_title * i + length_title)])
                for i in range(int(len(data_from_web) / length_title))]
    data_number = len(new_m_td)
    print(len(new_m_td[3]))  # 68
    print(type(new_m_td[3][0]))
    print(data_number)  # 4911
    print(new_m_td[3])
    # print(new_str_td)
    return new_m_td


def operate_mysql(message):
    conn = MySQLdb.connect("192.168.0.119", "root",
                           "root", "cloud_data", charset="utf8")
    cursor = conn.cursor()
    sql2 = "insert into specific_data values(%s, %s,%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s, \
%s, %s,%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s, \
%s, %s,%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s, %s, %s,\
%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)"
    print(message[0])
    try:
        cursor.executemany(sql2, message)
        conn.commit()
        conn.begin()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    start = datetime.datetime.now().replace(microsecond=0)
    message_number = get_links(home_url)
    operate_mysql(message_number)
    end = datetime.datetime.now().replace(microsecond=0)
    print('--------------------------')
    print('running time : {}'.format(end - start))
