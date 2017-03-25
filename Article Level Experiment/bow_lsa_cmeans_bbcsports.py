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
import skfuzzy as fuzz


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

    files = os.listdir(gen_path + category)
    files = [file for file in files if file.find('txt') > 0]
    for name in files:
        path = gen_path + category + '/' + name
        with open(path, 'r') as f:
            data = f.read()
        text.append(clean_str(data))
        cat_list.append(start)
    start += 1

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



r = np.transpose(reduced_matrix)

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    r, 5, 1.01, error=0.005, maxiter=1000, init=None)



cluster_membership = np.argmax(u, axis=0)
membership = np.ndarray.tolist(cluster_membership)

print cluster_membership
print cat_list
print p

# for c in range(len(categories)):
#     idx = np.where(labels==c)[0]
#     for l in idx:
#         result[l] = c+1
#
# print len(result)
# print result
#
score = normalized_mutual_info_score(membership, cat_list)
print score
adjusted_score = adjusted_mutual_info_score(cat_list, membership)
print adjusted_score