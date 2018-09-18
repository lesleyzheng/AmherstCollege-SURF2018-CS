from __future__ import print_function
import pickle
import sys
from sklearn import cluster
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import zero_one_loss
from sklearn.neighbors import KNeighborsClassifier
import statistics
import pandas as pd

'''
This document is used for finding clusters.

It takes in four command-line arguments, for now, only the first two is relevant:
1. file_name - the name of the matrix you wish to form clusters with, assumed to be in a sub data file
2. dict_name - a dictionary wtih url as key and news source label as value, assumed ot be in a sub data file
3. plot_status - whether or not you want to plot the fancy ass K-Means graph; write False for now
4. plot_clusters - in that plot, how many clusters would you like to form; its value doesn't matter for now

There will be some informative print statements. The most important one would be a summary table towards the end.

For now, I disabled plotting histograms for cluster distribution.

The most important part, however, is the outliers_url.pkl file that will be pickled out. It contains a list of 
urls that are outliers in all different clusterings. You can change the name of this output file on line 310.

Last updated: July 22, 2018
'''


class clustering(object):

    def __init__(self, filename, plot_status, plot_clusters):

        self.file_name = filename

        self.master = "3000_master_dict_8sources.pkl"

        self.df = pd.DataFrame(
            columns=['sample size', 'num of clusters', 'max', 'min', 'mean', 'median', 'mode',
                     '% of 0', '% of 1', '% of <10', '% of <100'])

        self.status = plot_status

        self.num_clusters = plot_clusters

        self.data = []

        self.ids = []

        self.labels = []

        self.outliers = set()

    def unpickle_matrix(self):

        pickle_in = open(f"./data/{self.file_name}.pkl", "rb")
        (matrix, ids), desc = pickle.load(pickle_in)
        pickle_in.close()
        print(f"completed unpickling of {self.file_name}\ndescription: {desc}\n\t...returning matrix and ids")
        matrix = np.array(matrix)
        ids = np.array(ids)
        self.data = matrix
        self.ids = ids

    def unpickle_dict(self):

        dict_in = open(f"./data/{self.master}", "rb")
        dictionary, description = pickle.load(dict_in)
        dict_in.close()
        print(f"completed unpickling of {self.master}\ndescription: {description}\n\t...returning master_dict\n")
        self.master = dictionary

    def make_labels(self, ids):

        for id in ids:
            self.labels.append(self.master[id])

        self.labels = np.array(self.labels)

    def plot(self, data, num_targets, sam_size):

        # plotting
        reduced_data = PCA(n_components=2).fit_transform(data)
        kmeans = KMeans(init='k-means++', n_clusters=num_targets, n_init=10)
        kmeans.fit(reduced_data)

        # decision boundary
        h = 0.02
        x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
        y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        plt.figure(1)
        plt.clf()
        plt.imshow(Z, interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   cmap=plt.cm.Paired,
                   aspect='auto', origin='lower')

        plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)

        # centroids
        centroids = kmeans.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)

        plt.title(f'{self.file_name} - KMeans for {num_targets} Clusters {sam_size} Sample Size')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())

        plt.show()

    def fit_KMean(self, num_targets, sam_size):

        # set up
        n_features = 0
        for i in range(len(self.data[0])):
            n_features += 1

        n_targets = num_targets

        n_samples = len(self.ids)

        sample_size = sam_size

        print("n_features: %d, \t n_targets: %d, \t n_samples: %d \t sample_size: %d"
              % (n_features, n_targets, n_samples, sample_size))

        # prepare data - randomization
        inds = [None] * n_samples
        for j in range(n_samples):
            inds[j] = j # create random list of numbers

        rs = np.random.RandomState(seed=sample_size)
        rs.shuffle(inds)

        X = self.data[inds, :]
        Y = self.labels[inds] # X's and Y's are now randomized and reduced to sample_size
        id = self.ids[inds]

        X = X[:sample_size]
        Y = Y[:sample_size]
        id = id[:sample_size]

        # KMeans
        cluster_model = KMeans(init='k-means++', n_clusters=num_targets, n_init=10).fit(X, Y) # future: change n_init?
        preds = cluster_model.predict(X)

        # distribution
        distribution = [None]*n_targets
        for k in range(n_targets):
            distribution[k] = []

        freq_distribution = [0]*n_targets

        zeros, ones, tens, hundreds, two_thousands = [], [], [], [], []

        # counter = 0
        for y in range(len(preds)):
            temp_idx = preds[y]
            temp_url = id[y]
            distribution[temp_idx].append(temp_url)
            # print("temp_idx %d \t temp_url %s" % (temp_idx, temp_url))
            # print(f"distribution of that idx is now {distribution[temp_idx]}")
            # counter += 1
            # if counter>10:
            #     break

            freq_distribution[temp_idx] += 1

        print(len(distribution))

        for i in range(len(distribution)):
            if len(distribution[i]) == 0:
                zeros.append(distribution[i])
            elif len(distribution[i]) == 1:
                ones.append(distribution[i])
            elif len(distribution[i]) < 10:
                tens.append(distribution[i])
            elif len(distribution[i]) < 100:
                hundreds.append(distribution[i])
            elif len(distribution[i]) > 2000:
                two_thousands.append(distribution[i])

        freq_distribution = np.array(freq_distribution)
        max = freq_distribution.max()
        min = freq_distribution.min()
        mean = freq_distribution.mean()
        median = statistics.median(freq_distribution)
        try:
            mode = statistics.mode(freq_distribution)
        except statistics.StatisticsError:
            mode = -1

        print(f"distribution {freq_distribution}")
        print(f"\n1's:")
        for one_url in ones:
            print(one_url)
            self.outliers.add(one_url[0])
        print(f"\n<10's:")
        for ten_url in tens:
            print(f"length {len(ten_url)}")
            print(ten_url)
        print(f"\n>2000's:")
        for two_t in two_thousands:
            print(f"length {len(two_t)}: {two_t[0]}, {two_t[1000]}, {two_t[2000]}")

        # adding to summary table
        self.df = self.df.append({'sample size': sample_size, 'num of clusters': n_targets, 'max': max,
                                  'min' : min, 'mean': mean, 'median': median, 'mode': mode,
                                  '% of 0': len(zeros)/sample_size, '% of 1': len(ones)/sample_size,
                                  '% of <10': len(tens)/sample_size, '% of <100': len(hundreds)/sample_size},
                                 ignore_index=True)

        return freq_distribution

    def start(self):

        self.unpickle_matrix()
        self.unpickle_dict()
        self.make_labels(self.ids)

        # original distribution
        original_dist = [0]*8

        zeros, ones, tens, hundreds = 0, 0, 0, 0

        for label in self.labels:
            original_dist[label] += 1

        for i in range(len(original_dist)):
            if original_dist[i] == 0:
                zeros += 1
            elif original_dist[i] == 1:
                ones += 1
            elif original_dist[i] < 10:
                tens += 1
            elif original_dist[i] < 100:
                hundreds += 1

        print(original_dist)
        print(150 * '-')

        # processing
        original_dist = np.array(original_dist)
        max = original_dist.max()
        min = original_dist.min()
        mean = original_dist.mean()
        median = statistics.median(original_dist)
        try:
            mode = statistics.mode(original_dist)
        except statistics.StatisticsError:
            mode = -1
        size = len(self.ids)

        # adding to summary table
        self.df = self.df.append({'sample size': size, 'num of clusters': 6, 'max': max,
                                  'min' : min, 'mean': mean, 'median': median, 'mode': mode, '% of 0': zeros/size,
                                  '% of 1': ones/size, '% of <10': tens/size, '% of <100': hundreds/size}, ignore_index=True)

        # KMean
        counter = 0
        for ssize in range(10000, 16001, 2000): # five times; 8000, 16001, 2000
            counter += 1
            subcounter = 1

            # histogram of original data
            # plt.figure(counter, figsize=(12, 8))
            # plt.subplot(231)
            # plt.hist(x=original_dist, rwidth=0.8)
            # plt.xlabel(f"number of articles in each of the 6 clusters")
            # plt.ylabel("frequency")
            # plt.title(f"Original Distribution")

            for nclusters in range(10, 71, 15): # three times; 10, 14, 1
                subcounter += 1
                print(f"\nCluster {nclusters} (sample size {ssize})")
                distr = list(self.fit_KMean(nclusters, ssize))
                print(150 * '-')

                # # histogram
                # subplot_dimension = int(str(23) + str(subcounter))
                # plt.subplot(subplot_dimension)
                # plt.hist(x=distr, bins=15, rwidth=0.8)
                # plt.xlabel(f"number of articles in each of the {nclusters} clusters")
                # plt.ylabel("frequency")
                # plt.title(f"Cluster {nclusters} (Sample Size {ssize}) Distribution")

            # plt.subplots_adjust(wspace=1, hspace=1)
            # plt.show()

        # present information
        print(self.df)

        # outliers
        print()
        print("outliers:")
        for outlier in self.outliers:
            print(outlier)
        print(f"size of set: {len(self.outliers)}")

        pickle_outliers = open(f"./data/{self.file_name}_outliers_full.pkl", "wb")
        message = f"this gives a list of {len(self.outliers)} outliers url from {self.file_name}"
        pickle.dump((list(self.outliers), message), pickle_outliers)
        pickle_outliers.close()

        plt.show

        # saving information
        # with open(f"./data/{self.file_name}_clustering_data.csv", "w") as f:
        #     self.df.to_csv(path_or_buf=f)
        # f.close()

        # # plot
        # print("plot!")
        # print(plot_status)
        # if plot_status == True:
        #     print("yes")
        #     print(plot_status)
        #     # self.plot(plot_num_clusters=plot_clusters)


if __name__ == "__main__":

    '''
    Matrices for Clustering
    - 3000_scaled_counts_content.pkl
    - 3000_scaled_collected_title.pkl
    Master Dict
    - 3000_master_dict_8sources.pkl
    '''

    # command line arguments
    file_name = str(sys.argv[1])
    plot_status = str(sys.argv[2])
    plot_clusters = int(sys.argv[3])

    # dealing with Boolean
    if plot_status == "True" or plot_status == "true" or plot_status == "t" or plot_status == "T":
        plot_status = True
    else:
        plot_status = False

    cluster = clustering(file_name, plot_status, plot_clusters)
    cluster.start()