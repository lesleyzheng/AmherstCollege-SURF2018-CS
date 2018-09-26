import pickle
import numpy as np
import sys
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap
from sklearn.preprocessing import StandardScaler

#runs PCA, t-SNE, or Isomap on a matrix and pickles it
def scaleMatrix(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)
    print("hi")
    return matrix_s

def runPCA(matrix, n, ids, name):
    matrix = np.array(matrix)
    pca = PCA(n_components=n)
    pca.fit(matrix)
    matrix = pca.transform(matrix)
    print(f"cumulative variation for {n} components is " + str(np.sum(pca.explained_variance_ratio_)))
    pickle_out = open(f"./data/pca_{n}_{name}.pkl", "wb")
    desc = f"pca to {n} dimesnions on {name}"
    pickle.dump(((matrix, ids), desc), pickle_out)
    pickle_out.close()

def runTSNE(matrix, n, ids, name):
    tsne = TSNE(n_components=n)
    matrix = tsne.fit_transform(matrix)
    # print(f"cumulative variation for {n} components is " + str(np.sum(tsne.explained_variance_ratio_)))
    pickle_out = open(f"./data/tsne_{n}_{name}.pkl", "wb")
    desc = f"tsne to {n} dimesnions on {name}"
    pickle.dump(((matrix, ids), desc), pickle_out)
    pickle_out.close()


def runISO(matrix, n, ids, name):
    iso = Isomap(n_neighbors = 10, n_components = n)
    matrix = iso.fit_transform(matrix)
    # print(f"cumulative variation for {n} components is " + str(np.sum(iso.explained_variance_ratio_)))
    pickle_out = open(f"./data/isomap_{n}_{name}.pkl", "wb")
    desc = f"isomap to {n} dimesnions on {name}"
    pickle.dump(((matrix, ids), desc), pickle_out)
    pickle_out.close()
    return matrix

if __name__ == '__main__':
    file_path = sys.argv[1] #matrix to run dim red on, should have list of ids with (dont give it scaled!)
    method = sys.argv[2] #pca, tsne, or isomap
    dim = int(sys.argv[3]) #dim to reduce it to
    name =sys.argv[4] #what to call the pickle file *see layout in method*

    pickle_in = open(file_path, "rb")
    (matrix, ids), desc = pickle.load(pickle_in)
    print(desc)
    matrix = scaleMatrix(matrix)

    if method == 'pca':
        runPCA(matrix, dim, ids, name)

    if method == 'tsne':
        runTSNE(matrix, dim, ids, name)

    if method == 'isomap':
        runISO(matrix, dim, ids, name)