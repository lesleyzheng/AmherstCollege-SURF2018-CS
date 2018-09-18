#from sklearn.manifold import TSNE
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#plots the matrix and identifies articles of interest
matrix_in = open('./data/5k_title_matrix.pkl', 'rb')
((matrix, ids), Y), desc = pickle.load(matrix_in)
matrix_in.close()

# eliminates the clump of articles with the title
# "News, Political Cartoons, Breaking News, Republican Election News, Conservative Facts, Commentary, Current Events"
# inds = [564,793,1154,1688,1791,2138,2826,2932,3014,3260,3282,3417,3483,3634,3783,4049,4074,4689,4930,4981,4984]

# eliminates above articles, and two other articles (inds 4805 and 4950) with extreme component values
# inds = [564,793,1154,1688,1791,2138,2826,2932,3014,3260,3282,3417,3483,3634,3783,4049,4074,4689,4805,4930,4950,4981,4984]

# eliminates the above articles, and two others with extreme values when the above are removed (4859 and 4974)
inds = [564,793,1154,1688,1791,2138,2826,2932,3014,3260,3282,3417,3483,3634,3783,4049,4074,4689,4805,4930,4950,4981,4984]

print(type(matrix))
print(type(Y))
i = len(inds)-1
while i >= 0:
    del matrix[inds[i]]
    i -= 1

Y = np.delete(Y, inds, axis = 0)

print("len ids:", len(inds))
print("len matrix: ", len(matrix))
print("len Y:", len(Y))
#
# label_in = open('./data/FakeNewsData.pkl', 'rb')
# (X,Y), desc_label = pickle.load(label_in)
# label_in.close()
# print('loaded')


scaler = StandardScaler()
scaler.fit(matrix)
matrix = scaler.transform(matrix)
pca = PCA(n_components = 2) # retains 95% of variance -- we can change this (this can also be the number of components/dimensions we want, eg. n_components = 3)
pca.fit(matrix)

matrix_pca = pca.transform(matrix)
print('pickling')

def findSpotInInds(i):
    for j in range(len(inds)):
        if i < inds[j]:
            print(f"my value is {i}")
            print(f"i am less than the {j} index of inds")
            print(f"i am returning {j}")
            return j
    print(f"my value is {i}")
    print('i am the largest value in inds')
    print(f"i am returning {len(inds)}")
    return len(inds)

for i in range(len(matrix_pca)):
    if matrix_pca[i][0] > 30:
        print("my component 1 is > 30")
        print(i + findSpotInInds(i))
    if matrix_pca[i][1] > 50:
        print("my component 2 is > 50")
        print(i + findSpotInInds(i))
    if matrix_pca[i][1] < -20:
        print("my component 2 is < -20")
        print(i + findSpotInInds(i))



print("index 4950: ",matrix_tsne[4950])
# pickle_out = open('./data/bow_pca_matrix.pkl', 'wb')
# pickle.dump(matrix_pca, pickle_out)
# pickle_out.close()

targets = [0,1]
colors = ['r', 'b']
for target, color in zip(targets,colors):
    inds_to_keep = []
    for i in range(len(Y)):
        if Y[i][2] == target:
            inds_to_keep.append(i)
    plt.scatter(matrix_pca[inds_to_keep, 0], matrix_pca[inds_to_keep, 1], alpha = 0.2,
            c = color, s = 50)
plt.xlabel('component 1')
plt.ylabel('component 2')

plt.show()
