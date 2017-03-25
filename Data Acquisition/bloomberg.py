import urllib2
from bs4 import BeautifulSoup
import socket
import httplib
from datetime import datetime
import json


class Bloomberg:
    BASEURL = "http://www.bloomberg.com/api/search?"
    end = ''

    def __init__(self, company, start, end):
        self.company = company
        self.start = start
        self.end = end

    def getData(self):


        curr_time = datetime.utcnow().strftime("%Y-%m-%d") + 'T' \
                    + datetime.utcnow().strftime("%H:%M:%S.%f")
        end = curr_time[0:len(curr_time) - 3] + 'Z'
        url = Bloomberg.BASEURL + "query=" + self.company.replace(' ', '+') + "&startTime=" + self.start + "&endTime=" + end
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().decode('utf-8')
        js = json.loads(data)
        pg_no = int(js['totalResults']/10) + 2
        items_all = []
        for i in range(1, pg_no):
            url = Bloomberg.BASEURL + "query=" + self.company.replace(' ', '+') + "&startTime=" + self.start + "&endTime=" + end \
                  + "&page=" + str(i)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            data = response.read().decode('utf-8')
            js = json.loads(data)
            items_all.extend(js['items'])

        return items_all


    def getNews(self):

        items_all = self.getData()
        fuzzy_name = self.company.split()
        headline_name = ''
        if len(fuzzy_name) == 1:
            headline_name = fuzzy_name[0]
        else:
            headline_name = fuzzy_name[1]
        list = []
        dict = {}
        # text_path = '/Users/HENGJIE/Desktop/text repo/Bloomberg/' + self.company + '/' + self.company + ' ' \
        #             + self.start + '-' + self.end + '.txt'
        text_path = '/Users/HENGJIE/Desktop/text repo/Bloomberg/' + self.company + '.txt'
        f = open(text_path, 'a')
        success = 0
        for item in items_all:
            if item['storyType'] == 'Article' and item.get('headline').lower().find(headline_name.lower()) >= 0:
                dict['url'] = item['url']
                dict['title'] = item['headline']
                request = urllib2.Request(item['url'])
                try:
                    html = urllib2.urlopen(request)
                except:
                    pass
                if html is not None:
                    news = ""
                    soup = BeautifulSoup(html, 'html.parser')
                    #technology
                    content = soup.select('section.main-column p')
                    if not content:
                        #market
                        content = soup.select('div.article-body__content > p')
                    if not content:
                        #view
                        content = soup.select('div._31WvjDF17ltgFb1fNB1WqY > p')
                    if not content:
                        #gadfly
                        content = soup.select('div.container_1KxJx > p')
                    for article in content:
                        if article.find(class_='inline-newsletter'):
                            continue
                        text = article.get_text()
                        if isinstance(text, basestring):
                            news = news + text.encode('utf8') + "\n"
                        else:
                            news = news + unicode(text).encode("utf8") + "\n"
                    dict['content'] = news

                list.append(dict.copy())
                success += 1
                print ("success {}".format(success))
            if success == 20:
                break


        json.dump(list, f, indent=4)
        return list, text_path





