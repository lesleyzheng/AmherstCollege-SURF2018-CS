import pickle
import nltk
import numpy as np
import matplotlib.pyplot as plt

#computes and plots the average number of sentences in the real and fake articles
def avg_sentences(list):
    #avg number of sentences in each article
    avg = 0
    for i in range(len(list)):
        sentences = nltk.sent_tokenize(list[i][3])
        avg = avg + len(sentences)
    avg = avg/len(list)
    return avg

finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)

avg_sent = avg_sentences(X)
print(f"There are an average of {avg_sent} sentences in the articles")

pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
avg_szero = avg_sentences(zero_list)
print(f"There is an average of {avg_szero} in the 0 articles")

pickle_in = open("./data/oneList.pkl", "rb")
one_list = pickle.load(pickle_in)
avg_sone = avg_sentences(one_list)
print(f"There is an average of {avg_sone} sentences in the 1 articles")
compare = [avg_szero, avg_sone]

# dict = {'whole': avg_sent, 'zero': avg_szero, 'one': avg_sone}
# pickle_out = open("./data/AvgSentences.pkl", "wb")
# pickle.dump(dict, pickle_out)
# pickle_out.close()

fig1 = plt.figure(1)
y_pos = np.arange(2)
plt.bar(y_pos, compare, align = 'center')
plt.xticks(y_pos, ('0', '1'))
plt.ylabel("average")
plt.xlabel("Article")
plt.title("Average number of sentences")
plt.show()
