import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from nltk.tokenize import sent_tokenize
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

path = '/Users/HENGJIE/Desktop/text repo/test data/apple.txt'

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

# LSA
# to be consistent with word embedding
svd = TruncatedSVD(50)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd,normalizer)
reduced_matrix = lsa.fit_transform(tfidf)
print type(reduced_matrix)

print reduced_matrix.shape
r = np.transpose(reduced_matrix)

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    r, 10, 1.05, error=0.005, maxiter=1000, init=None)

cluster_membership = np.argmax(u, axis=1)
membership = np.ndarray.tolist(cluster_membership)
print cluster_membership


seq = 0
for id in membership:
    strs = re.sub('&apos;',"'", sent_list_old[id])
    print 'Cluster ' + str(seq+1) + ': ' + strs + '\n\n'
    seq += 1


