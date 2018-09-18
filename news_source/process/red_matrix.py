import pickle
from random import Random
import sys


def reduc_rand(matrix_path, size, filename):
    # loading initial matrix
    matrix_in = open(matrix_path, 'rb')  # 10k_words_matrix.pkl
    matrix, desc = pickle.load(matrix_in)
    matrix_in.close()

    Random(1234).shuffle(matrix)

    matrix = matrix[:size]


    matrix_out = open(filename, 'wb')
    desc = f'randomized then reduced to specifized size {size}; returns three arguments: matrix, ids, and Y labels'
    pickle.dump((matrix, desc), matrix_out)
    matrix_out.close()

if __name__ == "__main__":
    matrix_path = sys.argv[1] #path of matrix you want to reduce
    size = int(sys.argv[2]) #size to reduce it to
    filename = str(sys.argv[3]) #name of file you want to save it as (do ./data)

    reduc_rand(matrix_path, size, filename)