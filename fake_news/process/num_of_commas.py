import pickle
import nltk
import numpy as np
import matplotlib.pyplot as plt

#computes and plots the average number of commas in the real and fake articles
def avg_commas(list):
    #avg number of commas in each article
    avg = 0
    for i in range(len(list)):
        count = 0
        words = nltk.word_tokenize(list[i][3])
        for i in range(len(words)):
            if words[i] == ',':
                count = count + 1
        avg = avg + count
    avg = avg / len(list)
    return avg

finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)

avg_com = avg_commas(X)
print(f"There are an average of {avg_com} commas in each word")

pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
avg_zcom = avg_commas(zero_list)
print(f"There are an average of {avg_zcom} commas in the 0 articles")

pickle_in = open("./data/oneList.pkl", "rb")
one_list = pickle.load(pickle_in)
avg_ocom = avg_commas(one_list)
print(f"There are an average of {avg_ocom} commas in each word in the 1 articles")


# dict = {'whole': avg_com, 'zero': avg_zcom, 'one': avg_ocom}
#
# pickle_out = open("./data/AvgCommas.pkl", "wb")
# pickle.dump(dict, pickle_out)
# pickle_out.close()


compare = [avg_zcom, avg_ocom]
y_pos = np.arange(2)
plt.bar(y_pos, compare, align = 'center')
plt.xticks(y_pos, ('0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.title("Average number of commas")
plt.show()