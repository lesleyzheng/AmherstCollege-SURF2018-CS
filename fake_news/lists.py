import pickle
import nltk

finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)

word_counts = []
comma_counts = []
sent_counts = []
for i in range(len(X)):
    words = nltk.word_tokenize(X[i][4])
    word_counts.append(len(words))
    commas = nltk.word_tokenize(X[i][3])
    count = 0
    for i in range(len(commas)):
        if commas[i] == ',':
            count = count + 1
    comma_counts.append(count)
    sentences = nltk.sent_tokenize(X[i][3])
    sent_counts.append(len(sentences))
print("done with whole set")


pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
word_zero = []
z_ccounts = []
z_scounts = []
for i in range(len(zero_list)):
    words = nltk.word_tokenize(zero_list[i][4])
    word_zero.append(len(words))
    commas = nltk.word_tokenize(zero_list[i][3])
    count = 0
    for i in range(len(commas)):
        if commas[i] == ',':
            count = count + 1
    z_ccounts.append(count)
    sentences = nltk.sent_tokenize(zero_list[i][3])
    z_scounts.append(len(sentences))
print("Done with zeros")


pickle_in = open("./data/oneList.pkl", "rb")
one_list = pickle.load(pickle_in)
word_one = []
o_ccounts = []
o_scounts = []
for i in range(len(one_list)):
    words = nltk.word_tokenize(one_list[i][4])
    word_one.append(len(words))
    commas = nltk.word_tokenize(one_list[i][3])
    count = 0
    for i in range(len(commas)):
        if commas[i] == ',':
            count = count + 1
    o_ccounts.append(count)
    sentences = nltk.sent_tokenize(one_list[i][3])
    o_scounts.append(len(sentences))
print("Done with ones")

all_lists = [word_counts, comma_counts, sent_counts, word_zero, z_ccounts, z_scounts, word_one, o_ccounts, o_scounts]
pickle_out = open('./data/allLists.pkl', 'wb')
pickle.dump(all_lists, pickle_out)
pickle_out.close()
print('pickled')