import pickle
import numpy as np
import matplotlib.pyplot as plt

#plots averages of real and fake news dataset
finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin)

num_of_articles = len(X)
print(f"There are {num_of_articles} articles")

pickle_in = open('./data/AvgWord.pkl', 'rb')
avg_word = pickle.load(pickle_in)
print(f"There are an average of {avg_word} word in the articles")

pickle_in = open('./data/Avg0Word.pkl', 'rb')
avg_zword = pickle.load(pickle_in)
print(f"There are an average of {avg_zword} word in the 0 articles")

pickle_in = open('./data/AvgOneWord.pkl', 'rb')
avg_oword = pickle.load(pickle_in)
print(f"There are an average of {avg_oword} word in the 1 articles")

pickle_in = open('./data/AvgSentences.pkl', 'rb')
sent_dict = pickle.load(pickle_in)
whole_s = sent_dict['whole']
zero_s = sent_dict['zero']
one_s = sent_dict['one']
print(f"There are an average of {whole_s} sentences in the articles")
print(f"There are an average of {zero_s} sentences in the 0 articles")
print(f"There are an average of {one_s} sentences in the 1 articles")

pickle_in = open('./data/AvgLetters.pkl', 'rb')
let_dict = pickle.load(pickle_in)
whole_l = let_dict['whole']
zero_l = let_dict['zero']
one_l = let_dict['one']
print(f"There are an average of {whole_l} letters in words in the articles")
print(f"There are an average of {zero_l} letters in words in the 0 articles")
print(f"There are an average of {one_l} letters in words in the 1 articles")

pickle_in = open('./data/AvgCommas.pkl', 'rb')
com_dict = pickle.load(pickle_in)
whole_c = com_dict['whole']
zero_c = com_dict['zero']
one_c = com_dict['one']
print(f"There are an average of {whole_c} commas in the articles")
print(f"There are an average of {zero_c} commas in the 0 articles")
print(f"There are an average of {one_c} commas in the 1 articles")

pickle_in = open('./data/AvgSentiments.pkl', 'rb')
sentiments = pickle.load(pickle_in)
compare = sentiments[0]
pickle_in = open('./data/AvgSent.pkl', 'rb')
avg_sent = pickle.load(pickle_in)
print(f"The sentiment value is {avg_sent} for the articles")
print(f"The sentiment value is {compare[0]} for the 0 articles")
print(f"The sentiment value is {compare[1]} for the 1 articles")

compare_w = [avg_word, avg_zword, avg_oword]
y_pos = np.arange(3)
fig1 = plt.figure(1)
plt.bar(y_pos, compare_w, align = 'center')
plt.xticks(y_pos, ('all','0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.title("Average number of words")

compare_s = [whole_s, zero_s, one_s]
fig2 = plt.figure(2)
y_pos = np.arange(3)
plt.bar(y_pos, compare_s, align = 'center')
plt.xticks(y_pos, ('all','0', '1'))
plt.ylabel("average")
plt.xlabel("Article")
plt.title("Average number of sentences")

compare_c = [whole_c,zero_c, one_c]
fig3 = plt.figure(3)
y_pos = np.arange(3)
plt.bar(y_pos, compare_c, align = 'center')
plt.xticks(y_pos, ('all','0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.title("Average number of commas")

compare_l = [whole_l, zero_l, one_l]
fig4 = plt.figure(4)
y_pos = np.arange(3)
plt.bar(y_pos, compare_l, align = 'center')
plt.xticks(y_pos, ('all', '0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.title("Average number of letters in each word")

fig5 = plt.figure(5)
y_pos = np.arange(3)
plt.bar(y_pos, [avg_sent, compare[0], compare[1]], align = 'center')
plt.xticks(y_pos, ('all','0', '1'))
plt.ylabel("Average")
plt.xlabel("Article")
plt.ylim(-1,1)
plt.title("Average sentiment of the articles")

# num = 0
# for i in range(len(sentiments[1])):
#     num = num + sentiments[1][i]
# num = num / len(sentiments[1])
# print(num)
# pickle_out = open('./data/AvgSent.pkl', 'wb')
# pickle.dump(num, pickle_out)
# pickle_out.close()

fig6 = plt.figure(6)
plt.hist(sentiments[1], 100)
plt.title("Frequency of sentiments")

fig7 = plt.figure(7)
plt.hist([sentiments[2], sentiments[3]], 50, label = ['0', '1'])
plt.legend(loc = 'upper center')
plt.title("Comparing the 0 and 1 sentiments")


pickle_in = open('./data/allLists.pkl', 'rb')
all_lists = pickle.load(pickle_in)
fig8 = plt.figure(8)
plt.hist(all_lists[0], 100)

plt.title("all words")

max = all_lists[0][0]
for i in range(1,len(all_lists[0])):
    if all_lists[0][i] > max:
        max = all_lists[0][i]
print(max)

plt.show()