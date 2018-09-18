import pickle
import time
import sys

def create_full(num):

    news_sources = ['blaze', 'cnn', 'huff', 'npr', 'time', 'brb', 'nr', 'reut']

    final_sorted = []

    count = 0

    for i in range(len(news_sources)):

        start_t = time.time()

        fp = open("./data/{1}_matrix/{0}_counts_{1}.pkl".format(news_sources[i], num), "rb")
        Sorted, desc = pickle.load(fp)
        fp.close()

        final_sorted += Sorted

        count += 1

        print("batch: ", count)
        tm = time.time()-start_t
        print("\ttime for batch {0}: {1}".format(count, tm))

    fx = open("./data/{1}_matrix/{1}_counts_{0}sources.pkl".format(len(news_sources), num), "wb")
    new_desc = ("concatenated all counts of ", str(news_sources))
    pickle.dump((final_sorted, new_desc), fx)
    fx.close()

if __name__ == "__main__":
    num = str(sys.argv[1])
    start_time = time.time()
    create_full(num)
    end_time = time.time()
    print("\ntotal duration: ", end_time-start_time)