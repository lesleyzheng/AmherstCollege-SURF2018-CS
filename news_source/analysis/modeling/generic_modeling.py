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
from sklearn.preprocessing import StandardScaler
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE

def unpickle(file):
    pickle_in = open(f"./data/{file}", 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    pickle_in.close()
    print(desc)

    # print(len(matrix))
    # print(len(matrix[0]))
    return (matrix, ids)


def runPCA(matrix, n, Y, ids):

    idxs = matrix_remove_outliers(ids)
    matrix = np.array(matrix)
    matrix = matrix[idxs, :]
    ids = np.array(ids)
    ids = ids[idxs]

    pca = PCA(n_components = n)
    pca.fit(matrix)
    matrix = pca.transform(matrix)
    print(f"cumulative variation for {n} components is " + str(np.sum(pca.explained_variance_ratio_)))
    if n == 2:
        graph(matrix, Y, ids)
        # plotKMeans(matrix)
        graph(matrix, Y, ids, 'pca', n)
    return matrix

def plotKMeans(data):

    # plotting
    num_targets = 8
    kmeans = KMeans(init='k-means++', n_clusters=num_targets, n_init=10)
    kmeans.fit(data)

    # decision boundary
    h = 0.02
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   cmap=plt.cm.Paired,
                   aspect='auto', origin='lower')

    plt.plot(data[:, 0], data[:, 1], 'k.', markersize=2)

    # centroids
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)

    plt.title(f'KMeans for {num_targets} Clusters (3000 counts content)')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())

    plt.show()

def matrix_remove_outliers(ids):

    '''
    - 3000_scaled_counts_content_outliers_full.pkl
    - 3000_scaled_counts_content_outliers.pkl
    - 3000_scaled_counts_title_outliers_full.pkl
    - 3000_scaled_counts_title_outlier.pkl
    '''

    pickle_outlier = open("./data/3000_scaled_counts_content_outliers_full.pkl", "rb")
    Outliers, description = pickle.load(pickle_outlier)
    pickle_outlier.close()

    outliers = set(Outliers)

    idx = []

    counter = 0
    for i in range(len(ids)):
        if ids[i] not in outliers:
            idx.append(i)
        else:
            counter += 1

    print("number of outliers: %d" % (counter))

    return list(idx)


def runTSNE(matrix, n, Y, ids, outliers = True):
    matrix = runPCA(matrix, n, Y, ids)

    tsne = TSNE(n_components=2)
    matrix = tsne.fit_transform(matrix)

    # plotKMeans(matrix)
    graph(matrix, Y, ids, 'tsne', n)
    return matrix

def run3dTSNE(matrix, n, Y, ids):
    matrix = runPCA(matrix, n, Y, ids)
    tsne = TSNE(n_components=3)
    matrix = tsne.fit_transform(matrix)
    graph3D(matrix, Y, ids)
    return matrix

def runISO(matrix, n, Y, ids, outliers = True):
    matrix = runPCA(matrix, n, Y, ids)


    matrix = Isomap(n_neighbors = 10, n_components = 2).fit_transform(matrix)
    graph(matrix, Y, ids, "iso", n)
    pickle_in = open('./data/testiso.pkl', 'wb')
    pickle.dump(matrix, pickle_in)
    pickle_in.close()
    return matrix


def graph(matrix, Y, ids, method, pca_to):
    news_sources = ['blaze', 'cnn', 'huff', 'npr', 'time', 'brb', 'nr', 'reut']
    targets = [0,1, 2, 3, 4, 5, 6, 7]
    # colors = ['r', 'b', 'm', 'g', 'c', 'k', 'y', (.7,.7,.7)]
    colors = ['r',
                  (31 / 255, 120 / 255, 180 / 255),
                  (122/255, 50/255, 200/255),
                  (51 / 255, 160 / 255, 44 / 255),
                  (1,.8,136/255),
                  'k',
                  'c',
                  (247/255, 129/255, 191/255) ]
    srcs = []
    for target, color in zip(targets,colors):
        inds_to_keep = []
        for i in range(len(matrix)):
            url = ids[i]
            if Y[url] == target: #and errors[i] == 1:
                inds_to_keep.append(i)
                srcs.append(news_sources[target])
        plt.scatter(matrix[inds_to_keep, 0], matrix[inds_to_keep, 1], label=news_sources[target], alpha = 0.5, marker = ".",
                c = color, s = 50)
    srcs = set(srcs)
    plt.title(f'pca to {pca_to} and {method} for sources {srcs}')
    plt.xlabel('component 1')
    plt.ylabel('component 2')
    plt.legend()
    plt.show()
    # plt.close()

def graph3D(matrix, Y, ids):
    news_sources = ['blaze', 'cnn', 'huff', 'npr', 'time', 'brb', 'nr', 'reut']
    targets = [0, 1, 2, 3, 4, 5, 6, 7]
    # colors = ['r', 'b', 'm', 'g', 'c', 'k', 'y', (.7, .7, .7)]
    colors = ['r',
                  (31 / 255, 120 / 255, 180 / 255),
                  (122/255, 50/255, 200/255),
                  (51 / 255, 160 / 255, 44 / 255),
                  (1,.8,136/255),
                  'k',
                  'c',
                  (247/255, 129/255, 191/255) ]
    ax = plt.axes(projection='3d')
    for target, color in zip(targets, colors):
        inds_to_keep = []
        for i in range(len(matrix)):
            url = ids[i]
            if Y[url] == target:  # and errors[i] == 1:
                inds_to_keep.append(i)
        ax.scatter(matrix[inds_to_keep, 0], matrix[inds_to_keep, 1], matrix[inds_to_keep, 2],
                   label=news_sources[target], alpha=0.5, marker=".",
                   c=color, s=50)
    plt.xlabel('component 1')
    plt.ylabel('component 2')
    plt.legend()
    plt.show()



def find_points(matrix, x1, x2, y1, y2, ids):
    for i in range(len(matrix)):
        if matrix[i][0] > x1 and matrix[i][0] < x2 and  matrix[i][1] > y1 and matrix[i][1] < y2:
            print(f"index {i} has a value of {ids[i]}")


def scaleMatrix(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)
    return matrix_s

def get_selection(all_matrix, all_ids, id_dict, targets):

    new_matrix = []
    new_ids = []

    for i in range(len(all_matrix)):
        if str(id_dict[all_ids[i]]) in targets:
            new_matrix.append(all_matrix[i])
            new_ids.append(all_ids[i])
    return new_matrix, new_ids

def run_logReg(matrix, uids, dict):
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

    num_train = length - 1000
    num_test = 1000

    X_tr = matrix[:num_train]
    Y_tr = Y[:num_train]
    X_te = matrix[num_train:num_train + num_test]
    Y_te = Y[num_train:num_train + num_test]

    print(f"Let's train a model on {num_train} points...")

    logReg = LogisticRegression()  # you can change solver and multiclass parameters
    logReg.fit(X_tr, Y_tr)
    print("Predictor ready!")
    train_preds = logReg.predict(X_tr)
    train_loss = zero_one_loss(Y_tr, train_preds)
    print(f"\tThe test loss is {train_loss} for our training data.")

    test_preds = logReg.predict(X_te)
    test_loss = zero_one_loss(Y_te, test_preds)

    print(f"\tThe test loss is {test_loss} for unseen data.")

    names = [f"Feature {i}" for i in range(len(X_tr[0]))]

    # from https://blog.datadive.net/selecting-good-features-part-iv-stability-selection-rfe-and-everything-side-by-side/
    rfe = RFE(logReg, n_features_to_select=1)
    rfe.fit(X_tr, Y_tr)
    print("Features sorted by rank")
    print(sorted(zip(map(lambda x: round(x, 4), rfe.ranking_), names)))

if __name__ == "__main__":

    pickle_in = open(f"./data/3000_matrix/3000_master_dict_8sources.pkl", 'rb')
    Y, desc = pickle.load(pickle_in)
    pickle_in.close()

    file = sys.argv[1]
    method = sys.argv[2]
    scaled = sys.argv[3] #if you're using a BOW matrix, this must be True
    pca_to = int(sys.argv[4])
    selection = sys.argv[5]


    matrix, ids = unpickle(file)

    matrix, ids = get_selection(matrix, ids, Y, selection)

    # run_logReg(matrix, ids, Y)

    if scaled == "False":
        matrix = scaleMatrix(matrix)


    if method == 'pca':
        matrix = runPCA(matrix, pca_to, Y, ids)

        # print("blue dot")
        # find_points(matrix, 1000, 1500, 800, 1000, ids)
        # print("---end---")
        # print("far right component 1")
        # find_points(matrix, 54, 62, -10, 30)
        # print("top component 2")
        # find_points(matrix, 10, 35, 23, 60)

    if method == 'tsne':
        matrix = runTSNE(matrix, pca_to, Y, ids, False)

    if method == '3dtsne':
        matrix = run3dTSNE(matrix, pca_to, Y, ids)

    if method == 'isomap':
        matrix = runISO(matrix, pca_to, Y, ids, False)
        # print("red dot")
        # find_points(matrix, 150, 170, -65, -50)
        # print()
        # find_points(matrix, -175, -150, 40, 60)
        # print()
        # find_points(matrix, -175, -150, -70, -40)

