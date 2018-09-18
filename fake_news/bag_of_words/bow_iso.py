from sklearn.decomposition import PCA
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn import manifold
from sklearn.ensemble import IsolationForest


#runs PCA to n components and then runs Isomap to 2 components for bag of words matrix
matrix_in = open('./data/new_5krand_matrix.pkl', 'rb')
(matrix, ids, labels), desc = pickle.load(matrix_in)
matrix_in.close()
print(len(matrix))
matrix = np.array(matrix)

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

#uncomment to run isolation forest and then change how the file is pickled out
# iso_f = IsolationForest(contamination = 0.05, random_state = 42)
# iso_f.fit(matrix_iso)
# preds = iso_f.predict(matrix_iso)
# print(len(preds))
# count = 0
# for i in range(len(preds)):
#     if preds[i] == 1:
#         count += 1
# print(count)

pickle_out = open('./data/isomap_5krand_forest5per.pkl', 'wb')
desc1 = 'isomap matrix on 5k rand words with PCA to 1000 and iso forest to 5per'
pickle.dump(((matrix_iso, ids, labels), desc1), pickle_out)
pickle_out.close()