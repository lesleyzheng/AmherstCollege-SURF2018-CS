'''Creates a master dictionary where the key is the index of the article
and the value is the corresponding label 1/0 indicating whether
or not the news article is fake news'''

import pickle
import collections

pickle_in = open("./data/FakeNewsData.pkl", "rb")
(X, Y), desc = pickle.load(pickle_in)
pickle_in.close()
print(desc)

print(len(X))
print(len(Y))
master = dict()#collections.defaultdict(lambda: -1)

first = 0

for i in range(len(X)):
    value = Y[i][2]
    master[i] = value

    # detect idx
    if first == 0:
        if i != X[i][0]:
            print(f"i is {i} but X has {X[i][0]}")
            print()
            first = 1
    else:
        if X[i][0] - X[i-1][0]>1:
            print(f"previous is {X[i-1][0]} current is {X[i][0]}")
            print()

print(len(master))

pickle_out = open("./data/masterdict.pkl", "wb")
description = "This is a dict of real_idx keys and label values"
pickle.dump((master, description), pickle_out)
pickle_out.close()
