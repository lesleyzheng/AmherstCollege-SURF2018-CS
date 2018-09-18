import pickle
import time
import sys

def create_full(num):

    news_sources = ['blaze', 'cnn', 'huff', 'npr', 'time', 'brb', 'nr', 'reut']

    final_sorted = []

    count = 0

    for i in range(len(news_sources)):

        start_t = time.time()

        fp = open("./data/{0}_matrix/{1}_sorted_collected_{0}.pkl".format(num, news_sources[i]), "rb")
        Sorted, desc = pickle.load(fp)
        fp.close()

        final_sorted += Sorted

        count += 1

        print("batch: ", count)
        tm = time.time()-start_t
        print("\ttime for batch {0}: {1}".format(count, tm))
    print(len(final_sorted))

    fx = open("./data/{0}_matrix/{0}_sorted_collected_{1}sources.pkl".format(num, len(news_sources)), "wb")
    new_desc = "concatenated {1} of sorted collected of {0}".format(str(news_sources), num)
    print(new_desc)
    pickle.dump((final_sorted, new_desc), fx)
    fx.close()

if __name__ == "__main__":

    num = sys.argv[1]

    start_time = time.time()
    create_full(num)
    end_time = time.time()
    tm = end_time-start_time
    print("\ntotal duration: {0}".format(tm))

