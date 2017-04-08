from django.shortcuts import render
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
from bloomberg import Bloomberg
from reuters import Reuters
from guardian import Guardian
from django.views.decorators.csrf import csrf_exempt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
from ner_class import NERClass
import json
import os
from datetime import datetime, timedelta, date
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from scipy import spatial
from spherecluster import SphericalKMeans
from sklearn.cluster import KMeans
matplotlib.use('Agg')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
@csrf_exempt

def index(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(BASE_DIR, "static_in_pro", "our_static")
    def word_in_text(word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        return False

    ## Extracting links for the tutorials
    def extract_link(text):
        regex = r'http://www\.reuters\.com/articles/[\w]+'
        match = re.search(regex, text)
        if match:
            return match.group()
        return ''

    text_ls = []
    per = []
    org = []
    loc = []
    if (request.POST):
        subject = request.POST["subject"]
        date = request.POST['date']
        date_range = request.POST['range']
        blm = Bloomberg(subject, date_range, date)
        articles = blm.getNews()
        for article in articles:
            text_ls.append(article['content'])
        ner = NERClass(articles)
        total_list = ner.execute_ner()
        per, org, loc = ner.freq_entities(total_list)

    return render(request, "index.html", {"total": "Article Count: " + str(len(text_ls)),
                                          "data_text":"<br/><br/>".join(text_ls),
                                          "top_persons": per,
                                          "top_organizations": org,
                                          "top_locations": loc})




def main(request):
    return render(request, 'main.html', {})





@csrf_exempt
def crawling(request):

   article_dict = {}

   if request.POST:
        subject = request.POST["subject"]
        date_range = request.POST['date_range']
        source = request.POST['source']
        articles = []
        address = ""
        if source == 'Bloomberg':
            temp = datetime.utcnow().strftime("%Y-%m-%d") + 'T' + datetime.utcnow().strftime("%H:%M:%S.%f")
            end_date = temp[0:len(temp) - 3] + 'Z'
            blm = Bloomberg(subject, date_range, end_date)
            articles, address = blm.getNews()

        elif source == 'Reuters':
            if date_range == "-1d":
                rts = Reuters(subject, 'pastDay')
                articles, address = rts.get_news()
            elif date_range == "-1w":
                rts = Reuters(subject, 'pastWeek')
                articles, address = rts.get_news()
            elif date_range == "-1m":
                rts = Reuters(subject, 'pastMonth')
                articles, address = rts.get_news()

        elif source == 'Guardian':
            end = date.today()
            if date_range == "-1d":
                time_delta = 1
                start = end - timedelta(time_delta)
                gdn = Guardian(subject, start, end, 1)
                articles, address = gdn.get_news()
            elif date_range == "-1w":
                time_delta = 7
                start = end - timedelta(time_delta)
                gdn = Guardian(subject, start, end, 1)
                articles, address = gdn.get_news()
            elif date_range == "-1m":
                time_delta = 30
                start = end - timedelta(time_delta)
                gdn = Guardian(subject, start, end, 1)
                articles, address = gdn.get_news()


        for article in articles:
            title = BeautifulSoup(article['title']).text
            article_dict[title] = article['content']

        request.session['address'] = address
        request.session['subject'] = subject
        request.session.set_expiry(300)
   return render(request, "crawling.html", {'news': article_dict})




@csrf_exempt
def summarization(request):
    def clean_str(string, TREC=False):
        """
        Tokenization/string cleaning for all datasets except for SST.
        Every dataset is lower cased except for TREC
        """
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        # string = re.sub(r"\(", " \( ", string)
        string = re.sub(r"\(", " ", string)
        # string = re.sub(r"\)", " \) ", string)
        string = re.sub(r"\)", " ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = re.sub(r"\d", " ", string)
        return string.strip() if TREC else string.strip().lower()

    text_ls = []
    per = []
    org = []
    loc = []
    context = {}

    if request.POST:
        subject = request.POST["subject"]
        path = request.POST['directory']
        with open(path, 'r') as f:
            articles = json.load(f)

        sent_list_old = []
        sent_list = []
        first_sent_idx = []

        for line in articles:
            sent_tokenize_list = sent_tokenize(line['content'])
            sent_tokenize_list = [item for item in sent_tokenize_list if item != '"\n']
            sent = map(lambda sentence: sentence.encode('ascii', 'ignore'), sent_tokenize_list)
            first_sent_idx.append(len(sent_list_old))
            sent_list_old += sent

        for sentence in sent_list_old:
            sent_list.append(clean_str(sentence))

        for article in articles:
            content = article['content']
            c = content.encode("utf-8")
            text_ls.append(c)
        ner = NERClass(articles, subject)
        total_list = ner.execute_ner()
        per, org, loc = ner.freq_entities(total_list, top=3)
        zipped_list = zip(per, org, loc)

        corpus = []
        title_dict = {}
        index = 0

        for article in articles:
            corpus.append(clean_str(article['content']))
            title_dict[str(index)] = BeautifulSoup(article['title']).text
            index += 1
        print (len(corpus))
        vectorizer = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
        count_vectorizer = vectorizer.fit_transform(corpus)
        transformer = TfidfTransformer(smooth_idf=True)
        tfidf = transformer.fit_transform(count_vectorizer)

        # LSA

        svd = TruncatedSVD(100)
        normalizer = Normalizer(copy=False)
        lsa = make_pipeline(svd, normalizer)
        reduced_matrix = lsa.fit_transform(tfidf)

        print reduced_matrix.shape

        # TSNE method
        # np.random.randint(1000, size=1)[0]
        model = TSNE(n_components=2, random_state=250)
        array = model.fit_transform(reduced_matrix)

        fig_dir =  os.path.join(BASE_DIR, "static_in_pro", "our_static")

        fig, ax = plt.subplots()
        print array.shape
        xlimvalue = np.max(np.abs(array[:,0]))*1.1
        plt.xlim(-xlimvalue, xlimvalue)
        ylimvalue = np.max(np.abs(array[:, 1]))*1.1
        plt.ylim(-ylimvalue, ylimvalue)
        plt.scatter(array[:, 0], array[:, 1])
        for key in title_dict.keys():
            plt.annotate(int(key), (array[:, 0][int(key)], array[:, 1][int(key)]),fontsize=20)

        frame1 = plt.gca()
        for xlabel_i in frame1.axes.get_xticklabels():
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
        for xlabel_i in frame1.axes.get_yticklabels():
            xlabel_i.set_fontsize(0.0)
            xlabel_i.set_visible(False)
        for tick in frame1.axes.get_xticklines():
            tick.set_visible(False)
        for tick in frame1.axes.get_yticklines():
            tick.set_visible(False)


        plt.title('TSNE Visualization')
        fig.savefig(fig_dir + "/img/test")
        dict_keys = []
        dict_values = []
        for i in range(len(title_dict)):
            dict_keys.append(i)
            dict_values.append(title_dict[str(i)])
        kv_list = zip(dict_keys, dict_values)



        # Multi-document summarization part

        vectorizer2 = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
        count_vectorizer2 = vectorizer2.fit_transform(sent_list)
        transformer2 = TfidfTransformer(smooth_idf=True)
        tfidf2 = transformer2.fit_transform(count_vectorizer2)
        print count_vectorizer2.shape


        # LSA
        # to be consistent with word embedding
        svd2 = TruncatedSVD(100)
        normalizer2 = Normalizer(copy=False)
        lsa2 = make_pipeline(svd2, normalizer2)
        reduced_matrix2 = lsa2.fit_transform(tfidf2)
        print type(reduced_matrix2)

        if len(articles) > 10:
            num_cluster = 10
        else:
            num_cluster = len(articles)

        # km = SphericalKMeans(num_cluster)
        # clusters = km.fit(reduced_matrix2)
        # centroids = km.cluster_centers_
        # labels = km.labels_
        # summa_index = []
        # for c in range(num_cluster):
        #     simi_list = []
        #     max_simi = -1 * float("inf")
        #     max_idx = -1
        #     centroid = centroids[c, :]
        #     idx = np.where(labels == c)[0]
        #     print idx
        #     for l in idx:
        #         simi = 1 - spatial.distance.cosine(centroid, reduced_matrix2[l, :])
        #         simi_list.append(simi)
        #     simi_list.sort(reverse=True)
        #     for l in idx:
        #         if len(sent_list_old[l].split()) <= 15:
        #             continue
        #         cos_simi = 1 - spatial.distance.cosine(centroid, reduced_matrix2[l, :])
        #         if l in first_sent_idx and cos_simi > simi_list[int(len(simi_list) * 0.3)] :
        #             # and cos_simi > simi_list[int(len(simi_list) * 0.9)]
        #             print 'bingo'
        #             max_idx = l
        #             break
        #         if cos_simi > max_simi:
        #             max_simi = cos_simi
        #             max_idx = l
        #     summa_index.append(max_idx)
        km = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=300, n_init=10, verbose=0)
        clusters = km.fit(reduced_matrix2)
        centroids = km.cluster_centers_
        labels = km.labels_
        summa_index = []
        for c in range(num_cluster):
            dist_list = []
            min_sum = float("inf")
            min_idx = -1
            centroid = centroids[c, :]
            idx = np.where(labels == c)[0]
            print idx
            for l in idx:
                dist = sum((centroid - reduced_matrix2[l, :]) ** 2)
                dist_list.append(dist)
            dist_list.sort()
            for l in idx:
                if len(sent_list_old[l].split()) <= 15:
                    continue
                dist = sum((centroid - reduced_matrix2[l, :]) ** 2)
                if l in first_sent_idx and dist < dist_list[int(len(dist_list) * 0.3)]:
                    print 'bingo'
                    min_idx = l
                    break
                if dist < min_sum:
                    min_sum = dist
                    min_idx = l
            summa_index.append(min_idx)
        print summa_index

        key_sen = []
        for id in summa_index:
            strs = re.sub('&apos;', "'", sent_list_old[id])
            key_sen.append(strs)

        context = {'persons': per,
                   'organizations': org,
                   'locations': loc,
                   'zip': zipped_list,
                   'kv': kv_list,
                   'key_sen': key_sen}

    elif 'subject' in request.session and 'address' in request.session:
        subject = request.session["subject"]
        path = request.session['address']
        with open(path, 'r') as f:
            articles = json.load(f)

        sent_list_old = []
        sent_list = []
        first_sent_idx = []

        for line in articles:
            sent_tokenize_list = sent_tokenize(line['content'])
            sent_tokenize_list = [item for item in sent_tokenize_list if item != '"\n']
            sent = map(lambda sentence: sentence.encode('ascii', 'ignore'), sent_tokenize_list)
            first_sent_idx.append(len(sent_list_old))
            sent_list_old += sent

        for sentence in sent_list_old:
            sent_list.append(clean_str(sentence))

        for article in articles:
            content = article['content']
            c = content.encode("utf-8")
            text_ls.append(c)
        ner = NERClass(articles, subject)
        total_list = ner.execute_ner()
        per, org, loc = ner.freq_entities(total_list, top=3)
        zipped_list = zip(per, org, loc)

        corpus = []
        title_dict = {}
        index = 0

        for article in articles:
            corpus.append(clean_str(article['content']))
            title_dict[str(index)] = BeautifulSoup(article['title']).text
            index += 1
        print (len(corpus))
        vectorizer = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
        count_vectorizer = vectorizer.fit_transform(corpus)
        transformer = TfidfTransformer(smooth_idf=True)
        tfidf = transformer.fit_transform(count_vectorizer)

        # LSA

        svd = TruncatedSVD(100)
        normalizer = Normalizer(copy=False)
        lsa = make_pipeline(svd, normalizer)
        reduced_matrix = lsa.fit_transform(tfidf)

        print reduced_matrix.shape

        # TSNE method
        # np.random.randint(1000, size=1)[0]
        model = TSNE(n_components=2, random_state=100)
        array = model.fit_transform(reduced_matrix)

        fig_dir = os.path.join(BASE_DIR, "static_in_pro", "our_static")

        fig, ax = plt.subplots()
        print array.shape
        xlimvalue = np.max(np.abs(array[:, 0])) * 1.1
        plt.xlim(-xlimvalue, xlimvalue)
        ylimvalue = np.max(np.abs(array[:, 1])) * 1.1
        plt.ylim(-ylimvalue, ylimvalue)
        plt.scatter(array[:, 0], array[:, 1])
        for key in title_dict.keys():
            plt.annotate(int(key), (array[:, 0][int(key)], array[:, 1][int(key)]), fontsize = 20)

        frame1 = plt.gca()
        for xlabel_i in frame1.axes.get_xticklabels():
            xlabel_i.set_visible(False)
            xlabel_i.set_fontsize(0.0)
        for xlabel_i in frame1.axes.get_yticklabels():
            xlabel_i.set_fontsize(0.0)
            xlabel_i.set_visible(False)
        for tick in frame1.axes.get_xticklines():
            tick.set_visible(False)
        for tick in frame1.axes.get_yticklines():
            tick.set_visible(False)

        plt.title('TSNE Visualization')
        fig.savefig(fig_dir + "/img/test")
        dict_keys = []
        dict_values = []
        for i in range(len(title_dict)):
            dict_keys.append(i)
            dict_values.append(title_dict[str(i)])
        kv_list = zip(dict_keys, dict_values)

        # Multi-document summarization part

        vectorizer2 = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
        count_vectorizer2 = vectorizer2.fit_transform(sent_list)
        transformer2 = TfidfTransformer(smooth_idf=True)
        tfidf2 = transformer2.fit_transform(count_vectorizer2)
        print count_vectorizer2.shape

        # LSA
        # to be consistent with word embedding
        svd2 = TruncatedSVD(100)
        normalizer2 = Normalizer(copy=False)
        lsa2 = make_pipeline(svd2, normalizer2)
        reduced_matrix2 = lsa2.fit_transform(tfidf2)
        print type(reduced_matrix2)

        if len(articles) > 10:
            num_cluster = 10
        else:
            num_cluster = len(articles)

        # km = SphericalKMeans(num_cluster)
        # clusters = km.fit(reduced_matrix2)
        # centroids = km.cluster_centers_
        # labels = km.labels_
        # summa_index = []
        # for c in range(num_cluster):
        #     simi_list = []
        #     max_simi = -1 * float("inf")
        #     max_idx = -1
        #     centroid = centroids[c, :]
        #     idx = np.where(labels == c)[0]
        #     print idx
        #     for l in idx:
        #         simi = 1 - spatial.distance.cosine(centroid, reduced_matrix2[l, :])
        #         simi_list.append(simi)
        #     simi_list.sort(reverse=True)
        #     for l in idx:
        #         if len(sent_list_old[l].split()) <= 15:
        #             continue
        #         cos_simi = 1 - spatial.distance.cosine(centroid, reduced_matrix2[l, :])
        #         if l in first_sent_idx and cos_simi > simi_list[int(len(simi_list) * 0.3)]:
        #             # and cos_simi > simi_list[int(len(simi_list) * 0.9)]
        #             print 'bingo'
        #             max_idx = l
        #             break
        #         if cos_simi > max_simi:
        #             max_simi = cos_simi
        #             max_idx = l
        #     summa_index.append(max_idx)
        km = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=300, n_init=10, verbose=0)
        clusters = km.fit(reduced_matrix2)
        centroids = km.cluster_centers_
        labels = km.labels_
        summa_index = []
        for c in range(num_cluster):
            dist_list = []
            min_sum = float("inf")
            min_idx = -1
            centroid = centroids[c, :]
            idx = np.where(labels == c)[0]
            print idx
            for l in idx:
                dist = sum((centroid - reduced_matrix2[l, :]) ** 2)
                dist_list.append(dist)
            dist_list.sort()
            for l in idx:
                if len(sent_list_old[l].split()) <= 15:
                    continue
                dist = sum((centroid - reduced_matrix2[l, :]) ** 2)
                if l in first_sent_idx and dist < dist_list[int(len(dist_list) * 0.3)]:
                    print 'bingo'
                    min_idx = l
                    break
                if dist < min_sum:
                    min_sum = dist
                    min_idx = l
            summa_index.append(min_idx)

        print summa_index

        key_sen = []
        for id in summa_index:
            strs = re.sub('&apos;', "'", sent_list_old[id])
            key_sen.append(strs)

        context = {'persons': per,
                   'organizations': org,
                   'locations': loc,
                   'zip': zipped_list,
                   'kv': kv_list,
                   'key_sen': key_sen}


    return render(request, 'summarization.html', context)