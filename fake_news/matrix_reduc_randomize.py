import pickle
import numpy as np
from random import Random
import sys


def reduc_rand(matrix, size, filename):
    # loading initial matrix
    matrix_in = open(f'./data/{matrix}', 'rb')  # 10k_words_matrix.pkl
    (matrix, ids), desc = pickle.load(matrix_in)
    matrix_in.close()

    # load Y
    finn = "./data/FakeNewsData.pkl"  # add in raw
    fin = open(finn, "rb")  # read, byte format
    (X, Y), des = pickle.load(fin)
    fin.close()

    labels = []
    for i in range(len(Y)):
        labels.append(Y[i][2])

    Random(1234).shuffle(ids)
    Random(1234).shuffle(matrix)
    Random(1234).shuffle(labels)

    ids = ids[:size]
    matrix = matrix[:size]
    labels = labels[:size]

    matrix = np.array(matrix)

    matrix_out = open(f'./data/{filename}', 'wb')
    desc = 'randomized then reduced to specifized size; returns three arguments: matrix, ids, and Y labels'
    pickle.dump(((matrix, ids, labels), desc), matrix_out)
    matrix_out.close()


if __name__ == "__main__":
    matrix = sys.argv[1]
    size = int(sys.argv[2])
    filename = str(sys.argv[3])

    reduc_rand(matrix, size, filename)




