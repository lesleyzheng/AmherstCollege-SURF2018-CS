from sklearn.ensemble import RandomForestClassifier
import pickle
import sys
import numpy as np

#uses RandomForestClassifier to find the most influential features in classifying
def run_rand_forest(matrix, uids, dict):


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

    num_train = length
    # num_test = 7000

    X_tr = matrix[:num_train]
    Y_tr = Y[:num_train]
    # X_te = matrix[num_train:num_train + num_test]
    # Y_te = Y[num_train:num_train + num_test]

    model = RandomForestClassifier(n_estimators = 100, max_features = 'auto', n_jobs = -1)
    model.fit(X_tr, Y_tr)

    names = [f"Feature {i}" for i in range(len(X_tr[0]))]

    # pickle_out = open('./data/randForest_list_whole.pkl', 'wb')
    # desc = ' list for 10000 bow matrix from random forest classfier'
    # pickle.dump((model.feature_importances_, desc), pickle_out)
    # pickle_out.close()

    print("Features sorted by rank")
    print(sorted(zip(map(lambda x: round(x, 4), model.feature_importances_), names), reverse = True))

if __name__ == '__main__':
    file_path = sys.argv[1]  # the path to the matrix
    label_dict_path = sys.argv[2]  # the path to the dictionary

    pickle_in = open(file_path, "rb")
    (matrix, uids), desc = pickle.load(pickle_in)
    print(len(matrix))

    dict_in = open(label_dict_path, "rb")
    labels, desc2 = pickle.load(dict_in)

    run_rand_forest(matrix, uids, labels)