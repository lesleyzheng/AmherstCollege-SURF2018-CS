import pickle
import numpy as np
import sys
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap
from sklearn.ensemble import IsolationForest
from sklearn.manifold import TSNE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import zero_one_loss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#runs PCA, t-SNE, or Isomap and plots the data
def unpickle(file):
    pickle_in = open("./data/{0}".format(file), 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    pickle_in.close()

    print(len(matrix))
    print(len(matrix[0]))
    return matrix

def runPCA(matrix,n, Y):
    pca = PCA(n_components = n)
    pca.fit(matrix)
    matrix = pca.transform(matrix)
    print("cumulative variation for ", n, " components is " + str(np.sum(pca.explained_variance_ratio_)))
    if n == 2:
        graph(matrix, Y)
    return matrix

def runTSNE(matrix, n, Y, outliers = True):
    matrix = runPCA(matrix, n, Y)
    if outliers:
        iso_f = IsolationForest(contamination=0.01, random_state=42)
        iso_f.fit(matrix)
        preds = iso_f.predict(matrix)
        inds_to_remove = []
        for i in range(len(preds)):
            if preds[i] == -1:
                inds_to_remove.append(i)
        matrix = [matrix[i] for i in range(len(matrix)) if i not in inds_to_remove]
        Y = [Y[i] for i in range(len(Y)) if i not in inds_to_remove]
    tsne = TSNE(n_components=2)
    matrix = tsne.fit_transform(matrix)
    graph(matrix, Y)

def runISO(matrix, n, Y, outliers = True):
    matrix = runPCA(matrix, n, Y)
    if outliers:
        iso_f = IsolationForest(contamination=0.01, random_state=42)
        iso_f.fit(matrix)
        preds = iso_f.predict(matrix)
        inds_to_remove = []
        for i in range(len(preds)):
            if preds[i] == -1:
                inds_to_remove.append(i)
        matrix = [matrix[i] for i in range(len(matrix)) if i not in inds_to_remove]
        Y = [Y[i] for i in range(len(Y)) if i not in inds_to_remove]

    matrix = Isomap(n_neighbors = 10, n_components = 2).fit_transform(matrix)
    graph(matrix, Y)
    return matrix

def graph(matrix, Y):
    targets = [0,1]
    colors = ['r', 'b']
    for target, color in zip(targets,colors):
        inds_to_keep = []
        for i in range(len(matrix)):
            if Y[i][2] == target: #and errors[i] == 1:
                inds_to_keep.append(i)
        plt.scatter(matrix[inds_to_keep, 0], matrix[inds_to_keep, 1], alpha = 0.2, marker = ".",
                c = color, s = 50)
    plt.xlabel('component 1')
    plt.ylabel('component 2')
    plt.savefig('./figs/plt1.png')
    plt.show()
    plt.close()

def find_points(matrix, x1, x2, y1, y2):
    for i in range(len(matrix)):
        if matrix[i][0] > x1 and matrix[i][0] < x2 and  matrix[i][1] > y1 and matrix[i][1] < y2:
            print("index ", i, " has a value of ", X[i][2], " and a location of ", matrix[i])


def scaleMatrix(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)
    return matrix_s

if __name__ == "__main__":

    pickle_in = open("./data/FakeNewsData.pkl", 'rb')
    (X, Y), desc = pickle.load(pickle_in)
    pickle_in.close()


    file = sys.argv[1]
    method = sys.argv[2]
    scaled = sys.argv[3]

    matrix = unpickle(file)
    if scaled == False:
        matrix = scaleMatrix(matrix)


    if method == 'pca':
        matrix = runPCA(matrix, 2, Y)


    if method == 'tsne':
        matrix = runTSNE(matrix, 10, Y, False)

    if method == 'isomap':
        matrix = runISO(matrix, 10, Y, False)
