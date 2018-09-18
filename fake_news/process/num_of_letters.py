import pickle
import nltk
import matplotlib.pyplot as plt
import numpy as np

#computes and plots the average number of letters in each word in the real and fake articles
def avg_letters(list):
    #avg number of letters in each word
    avg = 0
    num_of_words = 0
    for i in range(len(list)):
        words = list[i][4].split()
        num_of_words = num_of_words + len(words)
        for j in range(len(words)):
            avg = avg + len(words[j])
    avg = avg/num_of_words
    return avg


finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)

avg_let = avg_letters(X)
print(f"There are an average of {avg_let} letters in each word")

pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
avg_zlet = avg_letters(zero_list)
print(f"There are an average of {avg_zlet} letters in each word in the 0 articles")

pickle_in = open("./data/oneList.pkl", "rb")
one_list = pickle.load(pickle_in)
avg_olet = avg_letters(one_list)
print(f"There are an average of {avg_olet} letters in each word in the 1 articles")

# dict = {'whole': avg_let, 'zero': avg_zlet, 'one': avg_olet}
# pickle_out = open("./data/AvgLetters.pkl", "wb")
# pickle.dump(dict, pickle_out)
# pickle_out.close()

compare = [avg_zlet, avg_olet]
fig1 = plt.figure(1)
y_pos = np.arange(2)
plt.bar(y_pos, compare, align = 'center')
plt.xticks(y_pos, ('0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.title("Average number of letters in each word")
plt.show()