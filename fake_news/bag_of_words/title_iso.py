from sklearn.decomposition import PCA
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn import manifold
from sklearn.ensemble import IsolationForest

#runs Isomap on title bag of words matrix, plots it, and identifies articles of interest
def graph(matrix_iso, Y):
    targets = [0,1]
    colors = ['r', 'b']
    for target, color in zip(targets,colors):
        inds_to_keep = []
        for i in range(len(Y)):
            if Y[i][2] == target: #and errors[i] == 1:
                inds_to_keep.append(i)
        plt.scatter(matrix_iso[inds_to_keep, 0], matrix_iso[inds_to_keep, 1], alpha = 0.2, marker = ".",
                c = color, s = 50)
    plt.xlabel('component 1')
    plt.ylabel('component 2')

    plt.show()

def pickleit(matrix_iso, ids, Y, preds):
    pickle_out = open('../data/title_isomap_outliers_5krand_1per.pkl', 'wb')
    desc1 = 'isomap matrix and list of predictions from isolation forest with 0.01'
    pickle.dump(((matrix_iso, ids, Y, preds), desc1), pickle_out)
    pickle_out.close()

def IfNotCreated():
    matrix_in = open('../data/5k_title_matrix.pkl', 'rb')
    ((matrix, ids), Y), desc = pickle.load(matrix_in)
    matrix_in.close()
    print(len(matrix))
    print(type(matrix))

    print("loaded")
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)

    pca = PCA(n_components = 1000) # retains 95% of variance -- we can change this (this can also be the number of components/dimensions we want, eg. n_components = 3)
    pca.fit(matrix_s)
    # print(pca.n_components_)
    matrix_pca = pca.transform(matrix_s)
    print("cumulative variation for 1000 components is " + str(np.sum(pca.explained_variance_ratio_)) )
    print(type(matrix_pca))

    matrix_iso = manifold.Isomap(n_neighbors = 10, n_components = 2).fit_transform(matrix_pca)
    print("calculated")

    #running isolation forest
    iso_f = IsolationForest(contamination = 0.01, random_state = 42)
    iso_f.fit(matrix_iso)
    preds = iso_f.predict(matrix_iso)
    print(len(preds))
    # count = 0
    # for i in range(len(preds)):
    #     if preds[i] == 1:
    #         count += 1
    # print(count)

    pickleit(matrix_iso, ids, Y, preds)
    graph(matrix_iso, Y)


def ifCreated():
    matrix_in = open('../data/title_isomap_outliers_5krand_1per.pkl', 'rb')
    (matrix_iso, ids, Y, preds), desc1 = pickle.load(matrix_in)
    matrix_in.close()

    clump_GOOGLE = []
    clump1 = []
    clump2 = []
    clump3 = []
    for i in range(len(matrix_iso)):
        # if matrix_iso[i][0] > 80:
        #     print(f"index {i} has value of {matrix_iso[i]}")
        #     print(Y[i])
        if matrix_iso[i][0] > 21 and matrix_iso[i][0] < 21.5 and matrix_iso[i][1] > 20 and matrix_iso[i][1] < 21:
            clump_GOOGLE.append(i)
        if matrix_iso[i][0] > -7.05 and matrix_iso[i][0] < -7 and matrix_iso[i][1] > 8.5 and matrix_iso[i][1] < 9:
            clump1.append(i)
        if matrix_iso[i][0] > 26.08 and matrix_iso[i][0] < 26.1 and matrix_iso[i][1] > -18.65 and matrix_iso[i][1] < -18.6:
            clump2.append(i)
        if matrix_iso[i][0] > -5.2 and matrix_iso[i][0] < -5.14 and matrix_iso[i][1] > -0.62 and matrix_iso[i][1] < -0.61:
            clump3.append(i)
            #print(Y[i])
    print(clump_GOOGLE)
    print(clump1)
    print(clump2)
    print(clump3)
    graph(matrix_iso, Y)

if __name__ == '__main__':
    ifCreated()