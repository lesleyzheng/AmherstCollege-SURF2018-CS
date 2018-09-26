from sklearn.svm import LinearSVC
from sklearn.metrics import zero_one_loss
import numpy as np
import sys
import pickle
from sklearn.preprocessing import StandardScaler

#runs linear svc on a given matrix and prints the train and test loss
def runLinSVC(matrix, uids, dict):

    rs = np.random.RandomState(seed=1234)
    matrix = np.array(matrix)
    uids = np.array(uids)

    inds = [i for i in range(len(matrix))]

    rs.shuffle(inds)

    matrix = matrix[inds, :]
    uids = uids[inds]

    Y = []
    for id in uids:
        Y.append(dict[id])
    print(Y[0])
    Y = np.array(Y)

    length = len(matrix)

    num_train = length - 5000
    num_test = 5000

    X_tr = matrix[:num_train]
    Y_tr = Y[:num_train]
    X_te = matrix[num_train:num_train + num_test]
    Y_te = Y[num_train:num_train + num_test]

    print(f"Let's train a model on {num_train} points...")

    learner = LinearSVC()
    learner.fit(X_tr, Y_tr)
    print("\tDone!")
    train_preds = learner.predict(X_tr)

    train_loss = zero_one_loss(Y_tr, train_preds)
    print(f"The training loss is {train_loss}.")

    print(f"But let's test it on {num_test} previously unseen points:")

    test_preds = learner.predict(X_te)
    test_loss = zero_one_loss(Y_te, test_preds)

    print(f"\tThe test loss is {test_loss}.")

def scaleMatrix(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)
    return matrix_s


if __name__ == '__main__':
    file_path = sys.argv[1]  # the path to the matrix you want to run knn on
    label_dict_path = sys.argv[2]  # the path to the dictionary of labels that corrosponds to the matrix

    pickle_in = open(file_path, "rb")
    (matrix, uids), desc = pickle.load(pickle_in)
    print(len(matrix))

    dict_in = open(label_dict_path, "rb")
    labels, desc2 = pickle.load(dict_in)
    # matrix =scaleMatrix(matrix)

    runLinSVC(matrix, uids, labels)