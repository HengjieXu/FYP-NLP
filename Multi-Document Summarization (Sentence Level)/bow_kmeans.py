import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from nltk.tokenize import sent_tokenize
from sklearn.cluster import KMeans

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
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\(", " ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\)", " ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r"\d", " ", string)
    return string.strip() if TREC else string.strip().lower()

path = '/Users/HENGJIE/Desktop/text repo/test data/trump.txt'

with open(path, 'r') as f:
    lines = json.load(f)

sent_list_old = []
sent_list = []
first_sent_idx = []

for line in lines:
    sent_tokenize_list = sent_tokenize(line['content'])
    sent_tokenize_list = [item for item in sent_tokenize_list if item != '"\n']
    sent = map(lambda sentence: sentence.encode('ascii', 'ignore'), sent_tokenize_list)
    first_sent_idx.append(len(sent_list_old))
    sent_list_old += sent

print len(sent_list_old)

for sentence in sent_list_old:
    sent_list.append(clean_str(sentence))


print len(sent_list)

vectorizer = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
count_vectorizer = vectorizer.fit_transform(sent_list)
transformer = TfidfTransformer(smooth_idf=True)
tfidf = transformer.fit_transform(count_vectorizer)
print count_vectorizer.shape

arr = tfidf.toarray()

km = KMeans(n_clusters=10, init='k-means++', max_iter=300, n_init=10, verbose=0)
clusters = km.fit(arr)
centroids = km.cluster_centers_
labels =  km.labels_
summa_index = []
for c in range(10):
    dist_list = []
    min_sum = float("inf")
    min_idx = -1
    centroid = centroids[c, :]
    idx = np.where(labels==c)[0]
    print idx
    for l in idx:
        dist = sum((centroid - arr[l, :]) ** 2)
        dist_list.append(dist)
    dist_list.sort()
    for l in idx:
        if len(sent_list_old[l].split()) <= 6:
            continue
        dist = sum((centroid - arr[l, :]) ** 2)
        if l in first_sent_idx and dist < dist_list[int(len(dist_list) * 0.3)]:
            print 'bingo'
            min_idx = l
            break
        if dist < min_sum:
            min_sum = dist
            min_idx = l
    summa_index.append(min_idx)

print summa_index
seq = 0
for id in summa_index:
    strs = re.sub('&apos;',"'", sent_list_old[id])
    print 'Cluster ' + str(seq+1) + ': ' + strs + '\n\n'
    seq += 1
