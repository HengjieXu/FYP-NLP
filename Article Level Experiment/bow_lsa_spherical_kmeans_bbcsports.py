import os
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from spherecluster import SphericalKMeans


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


categories = ['athletics', 'cricket', 'football', 'rugby', 'tennis']
cat_list = []
start = 0
gen_path = '/Users/HENGJIE/Desktop/text repo/bbcsport/'
text = []
for category in categories:
    start += 1
    files = os.listdir(gen_path + category)
    files = [file for file in files if file.find('txt') > 0]
    for name in files:
        path = gen_path + category + '/' + name
        with open(path, 'r') as f:
            data = f.read()
        text.append(clean_str(data))
        cat_list.append(start)

result = np.zeros((1,len(cat_list)), dtype=np.int)
result = result.tolist()[0]

vectorizer = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
count_vectorizer = vectorizer.fit_transform(text)
transformer = TfidfTransformer(smooth_idf=True)
tfidf = transformer.fit_transform(count_vectorizer)

#LSA

svd = TruncatedSVD(100)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd,normalizer)
reduced_matrix = lsa.fit_transform(tfidf)

print reduced_matrix.shape

km = SphericalKMeans(n_clusters=len(categories))
clusters = km.fit(reduced_matrix)
centroids = km.cluster_centers_
labels =  km.labels_

for c in range(len(categories)):
    idx = np.where(labels==c)[0]
    for l in idx:
        result[l] = c+1

print len(result)
print result

score = normalized_mutual_info_score(cat_list, result)
adjusted_score = adjusted_mutual_info_score(cat_list, result)
print score
print adjusted_score
