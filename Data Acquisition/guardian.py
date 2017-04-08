#api key: 99b71d35-7fbf-4fb1-b58b-b0c25a18775a

import json
import urllib2
from bs4 import BeautifulSoup

class Guardian:
    BASEURL = 'http://content.guardianapis.com/search?q='

    def __init__(self, company, start, end, pn):
        self.company = company
        self.start = start
        self.end = end
        self.pn = pn

    def get_link(self, company, start, end, pn):

        subject = self.BASEURL + company.replace(" ", "+")
        pn = 'page=' + str(self.pn)
        str_date = 'from-date=' + str(start)
        end_date = 'to-date=' + str(end)
        pageSize = 'page-size=10'
        blocks = 'format=json&show-blocks=all'
        key = 'api-key=99b71d35-7fbf-4fb1-b58b-b0c25a18775a'
        link = [subject, str_date, end_date, pn, pageSize, blocks, key]
        url = '&'.join(link)
        print url
        return url

    def get_news(self):

        fuzzy_name = self.company.split()
        if len(fuzzy_name) == 1:
            headline_name = fuzzy_name[0]
        else:
            headline_name = fuzzy_name[1]

        link = self.get_link(self.company, self.start, self.end, self.pn)
        request = urllib2.urlopen(link)
        response = request.read()
        js = json.loads(response)
        num = js['response']['total']
        print int(num/10) + 1
        seqs = range(int(num/10) + 1)
        dict ={}
        list = []
        success = 0
        text_path = '/Users/HENGJIE/Desktop/text repo/Guardian/' + self.company + '.txt'
        f = open(text_path, 'w+')

        for seq in seqs:
            pn = 'page=' + str(seq+1)
            url = self.get_link(self.company, self.start, self.end, pn)
            req = urllib2.urlopen(url).read()
            res = req.strip('()')
            js = json.loads(res)
            results = js['response']['results']

            for result in results:
                if result['type'] == 'article':
                    value = True
                    headline = result['webTitle']
                    for item in list:
                        if item['title'] == headline:
                            value = False
                            break
                    if value:
                        if headline.lower().find(headline_name.lower()) >= 0:
                            dict['title'] = headline
                            dict['url'] = result['webUrl']
                            request = urllib2.Request(result['webUrl'])
                            html = urllib2.urlopen(request)
                            if html:
                                news = ""
                                soup = BeautifulSoup(html, 'html.parser')
                                content = soup.select('div.content__article-body > p')

                                for article in content:
                                    if article.find(class_='element-rich-link'):
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
                            if success == 10:
                                break

            if success == 10:
                break

        json.dump(list, f, indent=4)

        return list, text_path








