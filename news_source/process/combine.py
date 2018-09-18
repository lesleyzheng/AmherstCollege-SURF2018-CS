import pickle
import sys
import time

def create_pi_list(news_source, end_range, num):

    final_sorted = []

    count = 0
    for x in range(0, end_range, 100):
        start_t = time.time()
        fp = open("./data/{0}_matrix/{1}_process_{2}-{3}.pkl".format(num,news_source, x, x+100), "rb")
        temp_sort, desc = pickle.load(fp)
        final_sorted += temp_sort
        fp.close()
        count += 1
        tm = time.time()-start_t
        print("batch: {0}".format(count))
        print("\ttime for batch {0}: {1}".format(count, tm))

    fx = open("./data/{1}_matrix/{0}_sorted_collected_{1}.pkl".format(news_source, num), "wb")
    new_desc = f"{0} articles from {1}, processed".format(len(final_sorted), news_source)
    pickle.dump((final_sorted, new_desc), fx)
    fx.close()

if __name__ == "__main__":

    news_source = str(sys.argv[1])
    end_range = int(sys.argv[2])
    num = str(sys.argv[3])

    start_time = time.time()
    create_pi_list(news_source, end_range, num)
    end_time = time.time()
    tm = end_time-start_time
    print("\ntotal duration: {0}".format(tm))

