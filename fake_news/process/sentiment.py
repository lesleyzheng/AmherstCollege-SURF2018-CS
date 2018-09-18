import pickle
import nltk
import matplotlib.pyplot as plt
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#computes and plots the average sentiments of real and fake news articles
#plots the frequency of sentiments for real and fake news articles
#nltk.download('vader_lexicon')
finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)
print(desc)

num_of_articles = len(X)
print(f"There are {num_of_articles} articles")

print("The range for the articles is -1 being negative and 1 being positive")
analyzer = SentimentIntensityAnalyzer()
avg = 0
sents = []
num_pos = 0
num_neg = 0

for i in range(num_of_articles):
    score = analyzer.polarity_scores(X[i][3])
    sents.append(score['compound'])
    if score['compound'] > 0:
        num_pos = num_pos + 1
    if score['compound'] < 0:
        num_neg = num_neg + 1
    avg = avg + score['compound']
avg = avg / num_of_articles
print(f"The average sentiment for the articles is {avg}")
print(str((num_pos/num_of_articles) * 100) + " percent of the articles are positive")
print(str((num_neg/num_of_articles) * 100) + " percent of the articles are negative")
compare = []

#for 0s
z_sents = []
pickle_in = open("./data/zeroList.pkl", "rb")
zero_list = pickle.load(pickle_in)
num_pos = 0
num_neg = 0
avg = 0
for i in range(len(zero_list)):
    score = analyzer.polarity_scores(zero_list[i][3])
    z_sents.append(score['compound'])
    avg = avg + score['compound']
    if score['compound'] > 0:
        num_pos = num_pos + 1
    if score['compound'] < 0:
        num_neg = num_neg + 1
avg = avg / len(zero_list)
compare.append(avg)
print(f"The average sentiment for the  0 articles is {avg}")
print(str((num_pos/len(zero_list)) * 100) + " percent of the 0 articles are positive")
print(str((num_neg/len(zero_list)) * 100) + " percent of the 0 articles are negative")

#for 1s
pickle_in = open("./data/oneList.pkl", "rb")
ones = pickle.load(pickle_in)
o_sents = []
num_pos = 0
num_neg = 0
avg = 0
for i in range(len(ones)):
    score = analyzer.polarity_scores(ones[i][3])
    o_sents.append(score['compound'])
    avg = avg + score['compound']
    if score['compound'] > 0:
        num_pos = num_pos + 1
    if score['compound'] < 0:
        num_neg = num_neg + 1
avg = avg / len(ones)
compare.append(avg)
print(f"The average sentiment for the  1 articles is {avg}")
print(str((num_pos/len(ones)) * 100) + " percent of the 1 articles are positive")
print(str((num_neg/len(ones)) * 100) + " percent of the 1 articles are negative")


# to_pickle = [compare, sents, z_sents, o_sents]
# pickle_out = open('./data/AvgSentiments.pkl', 'wb')
# pickle.dump(to_pickle, pickle_out)
# pickle_in.close()


fig1 = plt.figure(1)
y_pos = np.arange(2)
plt.bar(y_pos, compare, align = 'center')
plt.xticks(y_pos, ('0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.ylim(-1,1)
plt.title("Average sentiment of the articles")
fig2 = plt.figure(2)
n, bins, patches = plt.hist(sents, 100)
plt.title("Frequency of sentiments")
fig3 = plt.figure(3)
n, bins, patches = plt.hist([z_sents, o_sents], 50, label = ['0', '1'])
plt.legend(loc = 'upper center')
plt.title("Comparing the 0 and 1 sentiments")
plt.show()
