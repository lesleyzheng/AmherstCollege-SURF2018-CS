import nltk
import pickle
from collections import defaultdict
import time
from nltk.corpus import stopwords
import sys
import random

#computes the 10,000 most common words in the article bodies and makes the bag of words matrix where there is 1 row for every article and 1 column for every word

def make_OED(processed):

    OED = defaultdict(int)

    for i in range(len(processed)):
        temp_dict = processed[i][25]
        print("============================At Index ", i, "============================")
        print(len(processed[i][25]))
        for k in temp_dict:
            OED[k] += temp_dict[k]

    all_words = []
    for k, v in OED.items():
        temp = [k, v]
        all_words.append(temp)

    stop_words = set(stopwords.words('english'))
    all_but_stop_words = [t for t in all_words if not t[0] in stop_words]

    # got sorted_by_second from https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
    sorted_by_second = sorted(all_but_stop_words, key=lambda tup: tup[1])

    top_10k = [None] * 10000
    index = len(sorted_by_second)-1
    for i in range(10000):
        top_10k[i] = (sorted_by_second[index][0])
        index-=1

    print(len(top_10k))
    pickle_out = open("./data/3000_matrix/bow_oed.pkl", "wb")
    pickle.dump(top_10k, pickle_out)
    pickle_out.close()
    return top_10k

def make_matrix(words , articles):
    list = [[None]] * len(articles)
    ids = []
    for i in range(len(articles)):
        temp_list = [None] * len(words)
        ids.append(articles[i][0])
        for w in range(len(words)):
            temp_list[w] = (articles[i][25][words[w]])
        list[i] = temp_list
    #print(list[0])
    return (list, ids)


if __name__ == '__main__':
    num = int(sys.argv[1])
    nltk.download('stopwords')
    pickle_in = open('./data/{0}_matrix/{0}_sorted_collected_8sources.pkl'.format(num), 'rb')
    processed, urls = pickle.load(pickle_in)
    print('loaded')
    print(len(processed))
   # print(processed[0][0])
    start = time.time()
    mega_words = make_OED(processed)
    end = time.time()
    print('dict made')
    matrix = make_matrix(mega_words, processed)
    pickle_out = open('./data/{0}_matrix/{0}_bow_content.pkl'.format(num), 'wb')
    desc = 'For the 8 news sources, a bag-of-words matrix from the content for sorted_collected.pkl. There are 10k columns, for most common words in all articles; 1 row for each article'
    pickle.dump((matrix, desc), pickle_out)
    pickle_out.close()

    print("runtime: ", end-start)
