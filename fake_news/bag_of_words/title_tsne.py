from sklearn.manifold import TSNE
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import zero_one_loss

#runs PCA to n components and then runs t-SNE to 2 components, plotting the resulting matrix
matrix_in = open('./data/5k_title_matrix.pkl', 'rb')
((matrix, ids), Y), desc = pickle.load(matrix_in)
matrix_in.close()


scaler = StandardScaler()

scaler.fit(matrix)
matrixp = scaler.transform(matrix)
pca = PCA(n_components = 1000) # retains 95% of variance -- we can change this (this can also be the number of components/dimensions we want, eg. n_components = 3)
pca.fit(matrixp)
# print(pca.n_components_)

matrix_pca = pca.transform(matrix)
print("cumulative variation for 1000 components is " + str(np.sum(pca.explained_variance_ratio_)) )

tsne = TSNE(n_components = 2)
matrix_tsne = tsne.fit_transform(matrix_pca)
print('fitted')

for i in range(len(matrix_tsne)):
    #isolating values to analyze, change numbers as needed
    if matrix_pca[i][0] > 15 and matrix_pca[i][0] < 15.02 and matrix_pca[i][1] < -18.5 and matrix_pca[i][1] > -18.6:
        print(f"index {i} has a value of {matrix_tsne[i]}")


targets = [0,1]
colors = ['r', 'b']
for target, color in zip(targets,colors):
    inds_to_keep = []
    for i in range(len(Y)):
        if Y[i][2] == target:
            inds_to_keep.append(i)
    plt.scatter(matrix_tsne[inds_to_keep, 0], matrix_tsne[inds_to_keep, 1], alpha = 0.4,
            c = color, s = 20)
print("computed")
plt.xlabel('component 1')
plt.ylabel('component 2')

plt.show()

pickle_out = open("./data/title_tsne_experiment.pkl", 'wb')
pickle.dump((matrix_tsne, Y), pickle_out)
pickle_out.close()
