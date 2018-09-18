import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
#import matplotlib.pyplot as plt

#runs PCA to n components and pickles the matrix
matrix_in = open('./data/10k_bow_matrix_correct.pkl', 'rb')
(matrix, ids), desc = pickle.load(matrix_in)
matrix_in.close()
print(len(matrix))

matrix = np.array(matrix)

print('loaded')

scaler = StandardScaler()
scaler.fit(matrix)
matrix = scaler.transform(matrix)
n = 1000
pca = PCA(n_components = n) # retains 95% of variance -- we can change this (this can also be the number of components/dimensions we want, eg. n_components = 3)
pca.fit(matrix)
print(f"cumulative variation for {n} components is " + str(np.sum(pca.explained_variance_ratio_)))


matrix_pca = pca.transform(matrix)
#uncomment to run isolation forest and then change how the file is pickled out
# iso_f = IsolationForest(contamination = 0.05, random_state = 42)
# iso_f.fit(matrix_pca)
# preds = iso_f.predict(matrix_pca)

print('pickling')
pickle_out = open('./data/10k_bow_pca_.pkl', 'wb')
desc1 = 'pca on 10k correct bow matrix to 1000 dims with list of uids'
pickle.dump(((matrix_pca, ids),desc1), pickle_out)
pickle_out.close()

