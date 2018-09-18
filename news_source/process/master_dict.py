import pickle
import time
import sys

def master(num):

    news_sources = ['blaze', 'cnn', 'huff', 'npr', 'time', 'brb', 'nr', 'reut'] # 0, 1, 2, 3, 4, 5, 6, 7
    master_dict = dict()

    for i in range(len(news_sources)):

        start_t = time.time()

        # load data
        pickle_in = open("./data/{1}_matrix/{0}_counts_{1}.pkl".format(news_sources[i],num), "rb")
        counts, desc = pickle.load(pickle_in)
        pickle_in.close()
        print(desc)

        for j in range(len(counts)):

            key = counts[j][0]
            master_dict[key] = i

        print("batch: ", i)
        tm = time.time()-start_t
        print("\ttime for batch {0}: {1}".format(i, tm))

    # save data
    pickle_out = open("./data/{1}_matrix/{1}_master_dict_{0}sources.pkl".format(len(news_sources),num), "wb")
    new_desc = "master dictionary with url as key and label as value, where " \
               "blaze = 0, cnn = 1, huff = 2, npr = 3, time = 4, brb = 5, nr = 6, reut = 7"
    pickle.dump((master_dict, new_desc), pickle_out)
    pickle_out.close()

    # print(master_dict)


if __name__ == "__main__":
    num = sys.argv[1]

    start = time.time()
    master(num)
    end = time.time()

    print("\ntotal duration: ", end-start)