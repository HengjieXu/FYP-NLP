import os
import re
import numpy as np
import cPickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.preprocessing import Normalizer
from sklearn.metrics.cluster import adjusted_mutual_info_score


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


def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    num_found = 0
    print ("Inside load_bin_vec function.")
    with open(fname, "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in range(vocab_size):
            word = []
            while True:
                ch = f.read(1)

                if ch == ' ':
                  word = ''.join(word)
                  break
                if ch != '\n':
                    word.append(ch)

            word = word.decode('utf-8','ignore')

            if word in vocab:
                num_found = num_found + 1
                word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
                print "Found word vector: " + word
            else:
                f.read(binary_len)

    print "words found: %d in total words: %d" %(num_found,len(vocab))
    return word_vecs


def add_unknown_words(word_vecs, vocab, k=300):
    """
    For words that occur in at least min_df documents, create a separate word vector.
    0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
    """
    for word in vocab:
        if word not in word_vecs:
            word_vecs[word] = np.random.uniform(-0.25,0.25,k)

def average_embedding(news, w2v, vocabulary, k=300):
    arr = np.empty((0, k))
    for new in news:
        new_embed = np.zeros((1, k))
        h = 0
        new = new.split(' ')
        for word in new:
            if word in vocabulary:
                new_embed = new_embed + w2v[word]
                h = h + 1
            # else:
            #     print word
        print float(h)/len(new)
        new_embed = new_embed / h
        arr = np.vstack([arr, new_embed])
        print 'success'
    return arr

def tfidf_matrix(matrix, w2v, glove, vocabulary):
    arr = np.empty((0,600))
    for word in vocabulary:
        if word in w2v.keys() and word in glove.keys():
            new_embed = w2v[word]
            adder = np.array(glove[word])
            combined = np.insert(adder, np.arange(len(new_embed)), new_embed)
            print len(combined)
            arr = np.vstack([arr, combined])
            print 'success'
        else:
            arr = np.vstack([arr, np.random.uniform(-0.25, 0.25, 600)])
            print 'failure'
    print arr.shape
    result = matrix * np.matrix(arr)
    result = np.array(result)
    return result

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

tfidf = TfidfVectorizer(strip_accents='ascii')
sparse_matrix = tfidf.fit_transform(text)
vocab = tfidf.get_feature_names()
print type(sparse_matrix)
print sparse_matrix.shape

print 'Vocabulary Loaded:'

pkl_file = open('/Users/HENGJIE/Desktop/text repo/bbcsport/w2v_bbc.pkl', 'rb')
w2v = cPickle.load(pkl_file)
pkl_file.close()

pkl_file = open('/Users/HENGJIE/Desktop/text repo/bbcsport/glove_bbc.pkl', 'rb')
glove = cPickle.load(pkl_file)
pkl_file.close()

# w2v = load_bin_vec('/Users/HENGJIE/Desktop/FYP Python/wv_google.bin',vocab)
print len(w2v)
print type(w2v)
print len(glove)
print type(glove)
print "Word Embeddings Loaded."


vectorizer = CountVectorizer(min_df=1, stop_words='english', strip_accents='ascii')
count_vectorizer = vectorizer.fit_transform(text)
transformer = TfidfTransformer(smooth_idf=True)
idf = transformer.fit_transform(count_vectorizer)

#LSA

svd = TruncatedSVD(300)
# normalizer = Normalizer(copy=False)
# lsa = make_pipeline(svd,normalizer)
reduced_matrix = svd.fit_transform(idf)

print reduced_matrix.shape

word_vec = tfidf_matrix(sparse_matrix, w2v, glove, vocab)
word_vec = np.hstack([word_vec, reduced_matrix])

print word_vec.shape
normalizer = Normalizer(copy=False)
word_vec = normalizer.fit_transform(word_vec)
km = KMeans(n_clusters=len(categories), init='k-means++', max_iter=300, n_init=10, verbose=0)

clusters = km.fit(word_vec)
labels = km.labels_

for c in range(len(categories)):
    idx = np.where(labels==c)[0]
    for l in idx:
        result[l] = c+1

print len(result)
print result

score = normalized_mutual_info_score(cat_list, result)
adjusted = adjusted_mutual_info_score(cat_list, result)
print score
print adjusted
