from nltk.tag.stanford import NERTagger
import json


def threshold(num, entities):
    filtered_outcome = [entity for entity in entities if entity[2] >= num]
    return filtered_outcome


# This method is to merge contiguous entities of the same type
def merge(tok):
    num_token = len(tok)
    i = 1
    while i < num_token:
        if tok[i][1] != 'O' and tok[i][1] == tok[i-1][1]:
            tok[i] = (tok[i - 1][0] + " " + tok[i][0], tok[i - 1][1])
            tok[i - 1] = (tok[i - 1][0], 'O')
        i += 1
    return tok


st = NERTagger('/Users/HENGJIE/Desktop/trydjango18/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
               '/Users/HENGJIE/Desktop/trydjango18/stanford-ner/stanford-ner.jar')
#path = '/Users/HENGJIE/Desktop/text repo/Bloomberg/donald trump/donald trump -1w-2017-03-03.txt'
path = '/Users/HENGJIE/Desktop/text repo/test data/samsung.txt'
total_list = [] # the list to store entities with document frequency

with open(path, 'r') as f:
    lines = json.load(f)
    filtered_lines = [line for line in lines if line['title'].find('Samsung') >= 0]
    print len(filtered_lines)

for line in filtered_lines:
    content = line['content']
    content = content.encode('utf-8', 'ignore')
    sentences = st.tag(content.split())
    article_list = [] # the list to store non-repeating entities within one article
    print len(sentences)
    for sentence in sentences:
        merge(sentence)
        for token in sentence:
            new = True
            i = 0
            # if token[0].lower() == 'ko' and token[1] == 'LOCATION':
            #     token = ('Korea', 'LOCATION')
            if token[1] != 'O':
                if(token[0] == 'Samsung Group'):
                    new = False
                # use document frequency instead of term frequency
                else:
                    for exist in article_list:
                        if exist[1] == 'PERSON' and token[1] == 'PERSON':
                            if token[0].lower() == exist[0].lower():
                                new = False
                                break
                        elif exist[1] == token[1]:
                            if exist[0].lower() in token[0].lower() or token[0].lower() in exist[0].lower():
                                new = False
                                if len(exist[0]) >= len(token[0]):
                                    article_list[i] = (token[0], token[1])
                                    break
                        i += 1
                if new:
                    article_list.append(token)

    # check whether entities in a particular article has already existed in the total list.
    for each in article_list:
        valid = True
        for previous in total_list:
            if previous[1] == 'PERSON' and each[1] == 'PERSON':
                if previous[0] == each[0]:
                    previous[2] += 1
                    valid = False
                    break
            elif previous[1] == each[1]:
                if previous[0].lower() in each[0].lower() or each[0].lower() in previous[0].lower():
                    previous[2] += 1
                    valid = False
                    if len(each[0]) <= len(previous[0]):
                        previous[0] = each[0]
                        break

        if valid:
            new_list = [each[0], each[1], 1]
            total_list.append(new_list)

total_list = threshold(1, total_list)
print len(total_list)
print total_list

