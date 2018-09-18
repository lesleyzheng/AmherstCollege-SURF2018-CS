from sklearn.manifold import TSNE
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

#runs PCA to n components and then runs t-SNE to 2 components on bag of words matrix
matrix_in = open('./data/new_5krand_matrix.pkl', 'rb')
(matrix, ids, labels), desc = pickle.load(matrix_in)
matrix_in.close()
print(len(matrix))
matrix = np.array(matrix)

scaler = StandardScaler()

scaler.fit(matrix)
matrix = scaler.transform(matrix)

pca = PCA(n_components = 100) # retains 95% of variance -- we can change this (this can also be the number of components/dimensions we want, eg. n_components = 3)
pca.fit(matrix)

matrix_pca = pca.transform(matrix)
print("cumulative variation for 1000 components is " + str(np.sum(pca.explained_variance_ratio_)) )
print('done with psa')

tsne = TSNE(n_components = 2)
matrix_tsne = tsne.fit_transform(matrix_pca)
print('fitted')


#uncomment to run isolation forest and then change how the file is pickled out
# iso_f = IsolationForest(contamination = 0.05, random_state = 42)
# iso_f.fit(matrix_tsne)
# preds = iso_f.predict(matrix_tsne)


pickle_out = open('./data/bow_tsne_5krand_points_removed.pkl', 'wb')
desc2 = 'tsne matrix on 5k rand words matrix with pca to 100 dimensions and 5per outliers removed'
pickle.dump(((matrix_tsne, ids, labels), desc), pickle_out)
pickle_out.close()

