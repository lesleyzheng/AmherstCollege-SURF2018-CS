import pickle
from collections import defaultdict
from nltk.corpus import stopwords
import sys


def excl_uids(processed):
    '''
    Deletes given uids
    '''

    # load data
    pickle_in2 = open("./data/odd_titles.pkl", "rb")
    odd_uid = pickle.load(pickle_in2)
    pickle_in2.close()

    end = len(processed) - 1

    OED = defaultdict(int)
    stop_words = set(stopwords.words('english'))

    i = 0
    while i < end:
        i += 1
        flag = True
        while flag == True:
            for uid in odd_uid:
                if processed[i][0] == uid:
                    odd_uid.remove(uid)
                    processed[i] = processed[end]
                    del processed[end]
                    end -= 1
                    break
            flag = False

        # Top Frequency Words
        temp_dict = processed[i][25]
        for k in temp_dict:
            if not k in stop_words:
                OED[k] += temp_dict[k]

    Sorted = sorted(OED.items(), key=lambda k_v: k_v[1], reverse=True)
    top = [None] * 10000
    for j in range(len(top)):
        top[j] = Sorted[j]

    print(f"Processed is now of size {len(processed)}")

    return processed, top


def avg(list):
    if isinstance(list, int):
        final = 0
    else:
        total = 0
        length = len(list)
        for i in range(len(list)):
            total += list[i]
        if total != 0:
            final = total / length
        else:
            final = 0

    return final


def make_matrix(proc, top):
    '''
    Creates large matrix for PCA etc.

    * - uid
    0 - avg number of letters in word in title
    1 - negativity of title
    2 - positivity of t
    3 - neu of ti
    4 - overall of ti
    5 - pos NOUN
    6 - pos VERB
    7 - pos ADJ
    8 - pos QUOTES
    9 - pos EXPLETIVES
    10 - neg
    11 - neu
    12 - pos
    13 - overall
    14+ 10,000 words

     - ne GEO
     -  ne PER
     - ne ORG

    '''

    lengs = len(proc)
    full_list = [None] * lengs
    uids = [None] * lengs

    for row in range(lengs):
        uids[row] = proc[row][0]

        temp = [None] * (10000 + 14)
        temp[0] = avg(proc[row][5])
        if len(proc[row][9]) == 4:
            temp[1] = proc[row][9][0]
            temp[2] = proc[row][9][1]
            temp[3] = proc[row][9][2]
            temp[4] = proc[row][9][3]
        else:
            temp[1] = 0
            temp[2] = 0
            temp[3] = 0
            temp[4] = 0
        temp[5] = len(proc[row][21]['NN'])
        temp[6] = len(proc[row][21]['VB'])
        temp[7] = len(proc[row][21]['JJ'])
        temp[8] = len(proc[row][21]['QUOTES'])
        temp[9] = len(proc[row][21]['EXPLETIVES'])
        if len(proc[row][24]) == 4:
            temp[10] = proc[row][24][0]
            temp[11] = proc[row][24][1]
            temp[12] = proc[row][24][2]
            temp[13] = proc[row][24][3]
        else:
            temp[10] = 0
            temp[11] = 0
            temp[12] = 0
            temp[13] = 0

        if len(proc[row][25]) != 0:
            for idx in range(len(top)):
                temp_word = top[idx][0]
                temp[14 + idx] = proc[row][25][temp_word]

        full_list[row] = temp

        if row % 1000 == 0:
            print(f"Finished {row} articles")

    print(f"full list length {len(full_list)}")

    return full_list, uids


def main_mod(filename):
    # Load Data
    pickle_in = open(f"./data/{filename}", "rb")
    processed = pickle.load(pickle_in)
    pickle_in.close()

    proc, top = excl_uids(processed)  # proc, top
    matrix, uid = make_matrix(proc, top)

    # Save Data
    pickle_out = open("./data/matrixv2.pkl", "wb")
    description = "matrix of avg number of letters per word in title, sentiments, avg number of expletives, etc. and top 10,000 words"
    pickle.dump(((matrix, uid), description), pickle_out)
    pickle_out.close()


if __name__ == "__main__":
    filename = sys.argv[1]

    # Run Main Module
    main_mod(filename)
