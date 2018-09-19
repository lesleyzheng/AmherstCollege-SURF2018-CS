from sklearn.linear_model import LogisticRegression
from sklearn.metrics import zero_one_loss
import pickle
import sys
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
import pickle

#runs linear regression on a given matrix and prints the train and test loss
#finds the top 3 and bottom 3 most influential features for classfication

def runLogR(matrix, uids, dict):

    # for i in range(len(matrix)):
    #     matrix[i] = matrix[i][:5000]
    # print(len(matrix[0]))

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

    logReg = LogisticRegression() #you can change solver and multiclass parameters
    logReg.fit(X_tr, Y_tr)
    print("Predictor ready!")
    train_preds = logReg.predict(X_tr)
    train_loss = zero_one_loss(Y_tr, train_preds)
    print(f"\tThe test loss is {train_loss} for our training data.")

    test_preds = logReg.predict(X_te)
    test_loss = zero_one_loss(Y_te, test_preds)

    print(f"\tThe test loss is {test_loss} for unseen data.")

    # find_top3(logReg)

    # names = [f"Feature {i}" for i in range(len(X_tr[0]))]
    #
    # #from https://blog.datadive.net/selecting-good-features-part-iv-stability-selection-rfe-and-everything-side-by-side/
    # rfe = RFE(logReg, n_features_to_select=100, step = 10)
    # rfe.fit(X_tr, Y_tr)
    # print("Features sorted by rank")
    # print(sorted(zip(map(lambda x: round(x,4), rfe.ranking_), names)))
    # pickle_out = open('./data/rfe_100_list.pkl', 'wb')
    # desc= ' list for 5000 bow matrix top 100'
    # pickle.dump((sorted(zip(map(lambda x: round(x,4), rfe.ranking_), names)),desc), pickle_out)
    # pickle_out.close()

def find_top3(logReg):
    list = []
    coefs = logReg.coef_

    for i in range(len(coefs)):
        all = []
        for j in range(len(coefs[0])):
            tup = (j, abs(coefs[i][j]))
            all.append(tup)
        all_sort = sorted(all, key = lambda tup: tup[1], reverse = True)
        length = len(all_sort)
        list.append((all_sort[0:3], all_sort[length-3:length]))
    for i in range(len(list)):
        print(f'Top 3 features for class {i}')
        print(list[i][0])
        print(f'Bottom 3 features for class {i}')
        print(list[i][1])

def scaleMatrix(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)
    return matrix_s

if __name__ == '__main__':
    file_path = sys.argv[1] #the path to the matrix you want to run knn on
    label_dict_path = sys.argv[2] #the path to the dictionary of labels that corrosponds to the matrix

    pickle_in = open(file_path, "rb")
    (matrix, uids), desc = pickle.load(pickle_in)
    print(len(matrix))

    dict_in = open(label_dict_path, "rb")
    labels, desc2 = pickle.load(dict_in)

    # matrix = scaleMatrix(matrix)

    runLogR(matrix, uids, labels)