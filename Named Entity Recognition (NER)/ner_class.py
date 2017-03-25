from nltk.tag.stanford import NERTagger
import json
import re
import sys


class NERClass:

    def __init__(self, dictionary, subject):
        self.dictionary = dictionary
        self.subject = subject


    def threshold(self, num, entities):
        filtered_outcome = [entity for entity in entities if entity[2] >= num]
        return filtered_outcome


    # This method is to merge contiguous entities of the same type such as: New (Org) York (Org) University (Org)
    def merge(self, tok):
        num_token = len(tok)
        i = 1
        while i < num_token:
            if tok[i][1] != 'O' and tok[i][1] == tok[i-1][1]:
                tok[i] = (tok[i - 1][0] + " " + tok[i][0], tok[i - 1][1])
                tok[i - 1] = (tok[i - 1][0], 'O')
            i += 1
        return tok

    def execute_ner(self):
        st = NERTagger('/Users/HENGJIE/Desktop/trydjango18/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/Users/HENGJIE/Desktop/trydjango18/stanford-ner/stanford-ner.jar')

        total_list = [] # the list to store entities with document frequency

        for line in self.dictionary:
            content = line['content']
            content = content.encode('utf-8', 'ignore')
            sentences = st.tag(content.split())
            article_list = [] # the list to store non-repeating entities within one article
            print len(sentences)
            for sentence in sentences:
                self.merge(sentence)
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

        return total_list


    def freq_entities(self, total_list, top=3):

        subject = self.subject
        fuzzy_name = self.subject.split()
        headline_name = ''
        if len(fuzzy_name) == 1:
            headline_name = fuzzy_name[0]
        else:
            headline_name = fuzzy_name[1]
        person_list = [element for element in total_list if
                       element[1] == 'PERSON' and re.search(headline_name.lower(), element[0].lower()) is None]
        person_list.sort(key=lambda x: x[2], reverse=True)
        per_name = []
        for per in person_list[0:top]:
            per_name.append(per[0])
        maxPerson = person_list[0][2]
        person_entities = []
        for seq in range(2, maxPerson):
            pruned = self.threshold(seq + 1, total_list)
            person_entities.append(len(pruned))

        # threshold test for organization
        org_list = [element for element in total_list if
                    element[1] == 'ORGANIZATION' and re.search(headline_name.lower(), element[0].lower()) is None]
        org_list.sort(key=lambda x: x[2], reverse=True)
        org_name = []
        for org in org_list[0:top]:
            org_name.append(org[0])
        maxOrg = org_list[0][2]
        org_entities = []
        for seq in range(2, maxOrg):
            pruned = self.threshold(seq + 1, total_list)
            org_entities.append(len(pruned))

        # threshold test for location
        loc_list = [element for element in total_list if
                    element[1] == 'LOCATION' and re.search(headline_name.lower(), element[0].lower()) is None]
        loc_list.sort(key=lambda x: x[2], reverse=True)
        loc_name = []
        for loc in loc_list[0:top]:
            loc_name.append(loc[0])
        maxLoc = loc_list[0][2]
        loc_entities = []
        for seq in range(2, maxLoc):
            pruned = self.threshold(seq + 1, total_list)
            loc_entities.append(len(pruned))

        return person_list[0:top], org_list[0:top], loc_list[0:top]


