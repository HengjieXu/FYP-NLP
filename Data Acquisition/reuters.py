import requests
import re
import urllib2
from bs4 import BeautifulSoup
import json

class Reuters:

    BASEURL = "http://www.reuters.com/assets/searchArticleLoadMoreJson"

    def __init__(self, company, date_range):
        self.company = company
        self.date_range = date_range

    def get_links(self):

        querystring = {"blob":self.company,"bigOrSmall":"big",
                       "articleWithBlog":"true","sortBy":"",
                       "dateRange":self.date_range,"numResultsToShow":"10",
                       "pn":"1","callback":"addMoreNewsResults"}

        response = requests.request("GET", self.BASEURL, params=querystring)

        info = response.text
        num = self.extract_num(info)
        print (num)
        querystring['numResultsToShow'] = str(num)
        querystring.pop('pn')
        response = requests.request("GET", self.BASEURL, params=querystring)
        links = self.extract_link(response.text)
        return links


    def get_news(self):

        fuzzy_name = self.company.split()
        if len(fuzzy_name) == 1:
            headline_name = fuzzy_name[0]
        else:
            headline_name = fuzzy_name[1]

        links = self.get_links()
        dict = {}
        list = []
        success = 0
        text_path = '/Users/HENGJIE/Desktop/text repo/Reuters/' + self.company + '.txt'
        f = open(text_path, 'w+')

        for link in links:
            link = 'http://www.reuters.com' + link
            request = urllib2.Request(link)
            value = True

            try:
                html = urllib2.urlopen(request)
                if html is not None:
                    news = ""
                    soup = BeautifulSoup(html, 'html.parser')
                    headline = soup.find('h1', 'article-headline').get_text()
                    for item in list:
                        if item['title'] == headline:
                            value = False
                            break

                    if value:

                        if headline.lower().find(headline_name.lower()) >= 0:
                            dict['title'] = headline
                            dict['url'] = link
                            #news = news + soup.select('span.article-prime > p')[0].get_text().encode('utf8') + '\n'
                            tag = soup.find('span', {"id": "article-text"})
                            m = tag.find_all("p")
                            for article in m:
                                text = article.get_text()
                                if isinstance(text, basestring):
                                    news = news + text.encode('utf8') + "\n"
                                else:
                                    news = news + unicode(text).encode("utf8") + "\n"
                            if len(news.split()) >= 100:
                                news = re.sub(r'\([^)]*\)', '', news)
                                dict['content'] = news
                                list.append(dict.copy())
                                print(link)
                                success += 1
                                print ("success {}".format(success))
                                if success == 10:
                                    break
                    else:
                        value = True
            except:
                pass


        json.dump(list, f, indent=4)
        return list, text_path



    def extract_link(self, info):
        regex = r'/article/[-\w]+'
        match = re.findall(regex, info)
        return match

    def extract_num(self, info):
        regex = r'totalResultNumber:\s[\d]+'
        match = re.findall(regex, info)
        num = re.findall(r'[\d]+', match[0])
        return int(num[0])


