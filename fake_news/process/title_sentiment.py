import pickle
import nltk
import numpy as np
import matplotlib.pyplot as plt

from nltk.sentiment.vader import SentimentIntensityAnalyzer

#computes and plots the average sentiment for real and fake news titles and then the frequency of sentiments for all the titles
def sent_title_analyzer(list):
    for i in range(len(list)):
        if list[i][2] == 'NaN' or isinstance(list[i][2], float) or len(list[i][2]) == 0:
            list[i][2] = ""
    analyzer = SentimentIntensityAnalyzer()
    sents = []
    count = 0
    avg = 0
    for i in range(len(list)):
        if list[i][2] != "":
            score = analyzer.polarity_scores(list[i][2])
            sents.append(score['compound'])
            count = count + 1
            avg = avg + score['compound']
        # if score['compound'] > 0:
        #     num_pos = num_pos + 1
        # if score['compound'] < 0:
        #     num_neg = num_neg + 1
    avg = avg/count
    return avg,sents


finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)
print(desc)

num_of_articles = len(X)
print(f"There are {num_of_articles} articles")

avg_title, scores = sent_title_analyzer(X)
print(f"The sentiment value for all the titles id {avg_title}")

pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
z_title, z_scores = sent_title_analyzer(zero_list)
print(f"The sentiment value for the 0 titles is {z_title}")

pickle_in = open("./data/oneList.pkl", "rb")
one_list = pickle.load(pickle_in)
o_title, o_scores = sent_title_analyzer(one_list)
print(f"The sentiment value for the 1 titles is {o_title}")



compare = [avg_title, z_title, o_title]
fig1 = plt.figure(1)
y_pos = np.arange(3)
plt.bar(y_pos, compare, align = 'center')
plt.xticks(y_pos, ('all','0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.ylim(-1,1)
plt.title("Average sentiment of the titles")

fig2 = plt.figure(2)
n, bins, patches = plt.hist(scores, 100)
plt.title("Frequency of sentiments for titles")
fig3 = plt.figure(3)
n, bins, patches = plt.hist([z_scores, o_scores], 50, label = ['0', '1'])
plt.legend(loc = 'upper center')
plt.title("Comparing the 0 and 1 sentiments for titles")
plt.show()