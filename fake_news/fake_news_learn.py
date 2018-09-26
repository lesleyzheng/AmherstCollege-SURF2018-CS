import pickle
from sklearn.neighbors import KNeighborsClassifier #a simple classifier
from sklearn.metrics import zero_one_loss
import sys
import numpy as np

#uses KNN to classify articles as real or fake
if __name__ == '__main__':
    filename = sys.argv[1]
    pickle_in = open(f'./data/{filename}', 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    matrix = np.array(matrix)

    rs = np.random.RandomState(seed=1234)
    num_points, num_dims = matrix.data.shape
    print(f"There are {num_points} points, each with {num_dims} dimensions")
    ids = np.array(ids)
    inds = [i for i in range(num_points)]
    rs.shuffle(inds)
    matrix = matrix[inds, :]
    ids = ids[inds]

    num_train = 100000
    num_test = len(matrix) - 100000

    X_tr = matrix[:num_train]
    Y_tr = ids[:num_train]
    X_te = matrix[num_train:num_train + num_test]
    Y_te = ids[num_train:num_train + num_test]

    print(f"Let's train a model on {num_train} points...")

    learner = KNeighborsClassifier(n_neighbors=3)
    learner.fit(X_tr, Y_tr)
    print("\tDone!")


    train_preds = learner.predict(X_tr)
    train_loss = zero_one_loss(Y_tr, train_preds)
    print(f"The training loss is {train_loss}.")

    print(f"But let's test it on {num_test} previously unseen points:")
    test_preds = learner.predict(X_te)
    test_loss = zero_one_loss(Y_te, test_preds)
    print(f"\tThe test loss is {test_loss}.")