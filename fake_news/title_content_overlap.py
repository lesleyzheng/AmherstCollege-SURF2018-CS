import pickle
from multiprocessing import Pool
from nltk.corpus import stopwords
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def analyze(idx):
    stops = stopwords.words('english')
    title_ex_stop = [W for W in matrix[idx][4] if W not in stops]
    content_ex_stop = set([w for w in matrix[idx][14] if w not in stops])
    total = len(title_ex_stop)
    intersect = len([word for word in title_ex_stop if word in content_ex_stop])

    if total != 0:
        temp = (intersect / total) * 100
    else:
        temp = 0

    return temp

if __name__ == "__main__":

    pickle_in = open("./data/sorted_collected.pkl", "rb")
    matrix = pickle.load(pickle_in)
    pickle_in.close()
    print("done loading pickle =D")

    # pickle_in = open("./data/process_4000-5000.pkl", "rb")
    # matrix, desc = pickle.load(pickle_in)
    # pickle_in.close()

    master_in = open("./data/masterdict.pkl", "rb")
    master, description = pickle.load(master_in)
    master_in.close()

    p = Pool(processes=32)
    analysis = p.map(analyze, range(len(matrix)))

    overlap = dict()
    class_z = []
    class_o = []

    for i in range(len(analysis)):
        if master[i] == 0:
            class_z.append(analysis[i])
        elif master[i] == 1:
            class_o.append(analysis[i])
        else:
            print("LABEL ERROR")
        overlap[i] = [analysis[i], master[i]]

    print("beginning to plot =D")
    n, bins, patches = plt.hist([class_z, class_o], bins=[0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 20.5, 30.5, 40.5, 50.5, 60.5, 70.5, 80.5, 90.5, 100.5], histtype='barstacked', color=['r', 'b'], label=['Class 0', 'Class 1'])
    M = max(n[0]) + max(n[1])
    plt.ylim(0, M)
    plt.legend()
    plt.savefig("./fig/title_content_overlap_2.png")
    # plt.show()

