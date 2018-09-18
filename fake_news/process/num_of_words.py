import nltk
import matplotlib.pyplot as plt
import numpy as np
import pickle

#nltk.download('punkt')

#computes and plots the average number of words in the real and fake articles
def avg_words(list):
    #finding average num of words
    avg = 0
    for i in range(len(list)):
        words = nltk.word_tokenize(list[i][4])
        avg = avg + len(words)
    avg = avg/len(list)
    # pickle_out = open("./data/AvgWord.pkl", "wb")
    # pickle.dump(avg, pickle_out)
    # pickle_out.close()
    #print(f"The average number of words in the articles is {avg}")
    return avg

finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)

num_of_articles = len(X)
print(f"There are {num_of_articles} articles")

avg = avg_words(X)
print(f"There is an average of {avg} words in the articles")

pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
print("There are " + str(len(zero_list)) + " 0 articles")

avg_zero = avg_words(zero_list)
print(f"There is an average of {avg_zero} words in the 0 articles")

pickle_in = open("./data/oneList.pkl", "rb")
one_list = pickle.load(pickle_in)
print(f"There are " + str(len(one_list)) + " 1 articles")

avg_one = avg_words(one_list)
print(f"There is an average of {avg_one} words in the 1 articles")

compare = [avg_zero, avg_one]
y_pos = np.arange(2)
fig1 = plt.figure(1)
plt.bar(y_pos, compare, align = 'center')
plt.xticks(y_pos, ('0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.title("Average number of words")
plt.show()
