import matplotlib.pyplot as plt
import pickle
from sklearn.ensemble import IsolationForest

#plots a desired matrix with correct labeling and colors

#if using a file with isolation forest preds add that to the tuple
matrix_in = open('./data/bow_tsne_5krand_points_removed.pkl', 'rb')  #
(matrix, ids, labels), desc = pickle.load(matrix_in) #errors


label_in = open('./data/FakeNewsData.pkl', 'rb')
(X,Y), desc_label = pickle.load(label_in)
label_in.close()
print(desc_label)

#uncomment to run isolation forest and then change how the file is pickled out
# iso_f = IsolationForest(contamination = 0.05, random_state = 42)
# iso_f.fit(matrix)
# preds = iso_f.predict(matrix)
#
# inds = []
# for i in range(len(preds)):
#     if preds[i] == -1:
#         inds.append(i)
# print(inds)
#
# pickle_out = open('./data/bow_tsne_5krand_forest5per.pkl', 'wb')
# desc = 'tsne on 5k rand with pca at 100 with list of preds at forest 5 percent'
# pickle.dump((matrix, preds, desc), pickle_out)
# pickle_out.close()

#this is for finding the articles in clusters
count = 0
for i in range(len(matrix)):
    if matrix[i][0] > 45 and matrix[i][0] < 55 and matrix[i][1] > 240 and matrix[i][1] < 246:
        uid = ids[i]
        #print(uid)
        for j in range(len(X)):
            if X[j][1] == uid:
                count += 1
                print(X[j])
                break

print(f'The count is {count}')
targets = [0,1]
colors = ['r', 'b']
for target, color in zip(targets,colors):
    inds_to_keep = []
    for i in range(len(labels)):
        if labels[i] == target: #and preds[i] == 1:
            inds_to_keep.append(i)
    plt.scatter(matrix[inds_to_keep, 0], matrix[inds_to_keep, 1], alpha = 0.2, marker = ".",
            c = color, s = 50)
plt.xlabel('component 1')
plt.ylabel('component 2')

plt.show()