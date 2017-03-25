import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer
import cPickle
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
                num_found += 1
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

def get_W(word_vecs, k=300):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """
    vocab_size = len(word_vecs)
    word_idx_map = dict()
    W = np.zeros(shape=(vocab_size, k))
    W[0] = np.zeros(k)
    i = 0
    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
        i += 1
    return W, word_idx_map


def compute_prob(path):
    with open(path, 'r') as f:
        articles = json.load(f)
    corpus = ''
    prob_dict = {}

    for article in articles:
        corpus += clean_str(article['content'].encode('ascii', 'ignore'))

    word_list = corpus.split()
    word_list = [item for item in word_list if item not in ['s', ',']]
    normalized = list(set(word_list))
    for word in normalized:
        count = word_list.count(word)
        prob_dict[word] = count / float(len(word_list))

    return prob_dict


def weighted_embedding(sentences, w2v, prob_dict, vocabulary, k=300, a = 0.001):
    arr = np.empty((0, k))
    for new in sentences:
        new_embed = np.zeros((1,k))
        h = 0
        new = new.split(' ')
        for word in new:
            if word in vocabulary:
                if word in prob_dict:
                    new_embed += float(a/(a+prob_dict[word])) * w2v[word]
                else:
                    new_embed += w2v[word]
                    print 'not success'
                h += 1

        if h != 0:
            print 'success'
            new_embed = new_embed/h
        arr = np.vstack([arr, new_embed])
    return arr

def g_weighted_embedding(sentences, w2v, prob_dict, vocabulary, k=300, a = 0.001):
    arr = np.empty((0, k))
    for new in sentences:
        new_embed = np.zeros((1,k))
        h = 0
        new = new.split(' ')
        for word in new:
            if word in vocabulary:
                if word in prob_dict:
                    new_embed += a/(a+prob_dict[word]) * np.array(w2v[word])
                else:
                    new_embed += w2v[word]
                    print 'not success'
                h += 1

        if h != 0:
            print 'success'
            new_embed = new_embed/h
        arr = np.vstack([arr, new_embed])
    return arr

path = '/Users/HENGJIE/Desktop/text repo/test data/apple.txt'

probability = compute_prob(path)

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

for sentence in sent_list_old:
    sent_list.append(clean_str(sentence))

vectorizer = CountVectorizer(min_df=1, strip_accents='ascii')
sparse_matrix = vectorizer.fit_transform(sent_list)
vocab = vectorizer.get_feature_names()
print len(vocab)
print 'Vocabulary Loaded:'

pkl_file = open('/Users/HENGJIE/Desktop/text repo/Bloomberg/samsung/w2v_nonmean.pkl', 'rb')
w2v = cPickle.load(pkl_file)
pkl_file.close()
# w2v = load_bin_vec('/Users/HENGJIE/Desktop/FYP Python/wv_google.bin',vocab)
print len(w2v)
print type(w2v)
print "Word Embeddings Loaded."
add_unknown_words(w2v, vocab, k=300)

pkl_file = open('/Users/HENGJIE/Desktop/text repo/Bloomberg/samsung/glove_nonmean.pkl', 'rb')
glove = cPickle.load(pkl_file)
pkl_file.close()
print len(glove)
print type(glove)
print "Word Embeddings Loaded."
add_unknown_words(glove, vocab, k=300)


results = weighted_embedding(sent_list, w2v, probability, vocab)
outcome = g_weighted_embedding(sent_list, glove, probability, vocab)
print results.shape

pca_model = PCA(n_components=100)
pca_model.fit(results)
componets_matrix = pca_model.components_

u = np.matrix(componets_matrix[0,:])
u_t = np.transpose(u)
adjust_term = results*u_t*u
print adjust_term.shape
results = results - adjust_term
results = np.array(results)

p_model = PCA(n_components=100)
p_model.fit(outcome)
c_matrix = pca_model.components_

u1 = np.matrix(c_matrix[0,:])
u1_t = np.transpose(u1)
adjust = outcome*u1_t*u1
print adjust.shape
outcome = outcome - adjust
outcome = np.array(outcome)

word_vec = np.hstack([results, outcome])
print word_vec.shape
normalizer = Normalizer(copy=False)
word_vec = normalizer.fit_transform(word_vec)

r = np.transpose(word_vec)

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