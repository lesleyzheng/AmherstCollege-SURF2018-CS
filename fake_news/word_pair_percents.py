from collections import defaultdict
import pickle
from nltk.corpus import stopwords
import sys
from multiprocessing import Pool
from functools import partial
import time

#computes the percentages that pairs of words appear together in the articles and saves that as a matrix for real articles and fake articles
def make_OED(processed):

    OED = defaultdict(int)

    for i in range(len(processed)):
        temp_dict = processed[i][25]
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

    top_10k = [None] * 1000
    index = len(sorted_by_second)-1
    for i in range(1000):
        top_10k[i] = (sorted_by_second[index][0])
        index-=1

    print(len(top_10k))
    return top_10k

def iterate_words(word, processed, top_10k):
    start = time.time()
    temp = [None] *1000
    for j in range(len(top_10k)):
        count = 0
        arts = 0
        other = top_10k[j]
        for a in range(len(processed)):
            list_words = processed[a]
            if word in list_words:
                arts += 1
                if other in list_words:
                    count += 1
        percent = (count / arts) * 100
        temp[j] = percent
    print(word)
    end = time.time()
    print(f'start at {start} and end at {end}')
    return temp

def rem_stopwords(processed):
    temp_list = [None] * len(processed)
    for i in range(len(processed)):
        list_words = processed[i][14]
        stop_words = set(stopwords.words('english'))
        list_words = [t for t in list_words if not t in stop_words]
        temp_list[i] = list_words
    return temp_list



if __name__ == '__main__':
    filename = sys.argv[1]
    save_as_z = sys.argv[2]
    save_as_o = sys.argv[3]
    pickle_in = open(f'./data/{filename}', 'rb')
    (processed, ids, labels), desc = pickle.load(pickle_in)
    print(len(processed))
    print(processed[0][0])

    zeros = [processed[i] for i in range(len(processed)) if labels[i] ==0]
    ones = [processed[i] for i in range(len(processed)) if labels[i] == 1]
    print('lists made')

    list_10k_zero = make_OED(zeros)
    list_10k_ones = make_OED(ones)
    print('1000 made')

    no_stopwords_zero = rem_stopwords(zeros)
    no_stopwords_ones = rem_stopwords(ones)
    print('done with stopwords')

    print(len(no_stopwords_zero))
    start_pool = time.time()
    p = Pool(processes = 64)  # how many?
    foo = partial(iterate_words, processed = no_stopwords_zero, top_10k = list_10k_zero)
    matrix = p.map(foo, list_10k_zero)
    print('matrix done')
    end_pool = time.time()
    print(f'started at {start_pool} and ended at {end_pool}')

    pickle_out = open(f'./data/{save_as_z}', 'wb')
    desc2 = 'percentage that a pair of words appears in the articles as a matrix and the list of the top 1000 words, ids, and labels'
    pickle.dump(((matrix, list_10k_zero),desc2), pickle_out)
    pickle_out.close()

    print('starting ones')

    print(len(no_stopwords_ones))
    start_pool2 = time.time()
    p2 = Pool(processes=64)  # how many?
    foo2 = partial(iterate_words, processed=no_stopwords_ones, top_10k=list_10k_ones)
    matrix2 = p2.map(foo2, list_10k_ones)
    print('matrix2 done')
    end_pool2 = time.time()
    print(f'started at {start_pool2} and ended at {end_pool2}')

    p_out = open(f'./data/{save_as_o}', 'wb')
    desc3 = 'percentage that a pair of words appears in the articles as a matrix and the list of the top 1000 words, ids, and labels'
    pickle.dump(((matrix2, list_10k_ones), desc3), p_out)
    p_out.close()

    print('done')
