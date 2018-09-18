''''
This is used for the analysis of article titles
'''

import pickle
import pandas as pd
import nltk
import string
import collections
import matplotlib.pyplot as plt

finn = "./data/FakeNewsData.pkl"
fin = open(finn, "rb") #read, byte format
(X, Y), desc = pickle.load(fin) #de-serialize a data stream; to serialize, call dumps()
print(desc)

def clean(s):
    tokens = [w.lower() for w in nltk.word_tokenize(s)]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    return stripped

def pandas_df(X):

    num_articles = len(X)
    print(f"There are {num_articles} in total.")

    all = []
    conc_titles = []

    for i in range(num_articles):

        inds = []

        inds.append(str(X[i][1]))
        if X[i][2] == 'NaN' or isinstance(X[i][2], float) or len(X[i][2]) == 0:
            inds.append("00000000")
            inds.append("00000000")
            inds.append(0)
            conc_titles.append("00000000")
        else:
            title = clean(X[i][2])
            concatenated = "".join(title)
            inds.append(title)
            inds.append(concatenated)
            inds.append(len(title))
            conc_titles.append(concatenated)
        inds.append(X[i][4])

        all.append(inds)

    return conc_titles, all

def len_analysis(df):

    # Distribution of short titles
    zero_title = df.loc[lambda df: df.len_title == 0]
    one_title = df.loc[lambda df: df.len_title == 1]
    two_title = df.loc[lambda df: df.len_title == 2]
    three_title = df.loc[lambda df: df.len_title == 3]
    four_title = df.loc[lambda df: df.len_title == 4]

    title_lens = [len(zero_title), len(one_title), len(two_title), len(three_title), len(four_title)]
    print(f"There are {title_lens} of zero, one, two, three, and four lengthed titles, respectively")
    zero_title.to_csv("./data/odd_titles/zero_title")
    one_title.to_csv("./data/odd_titles/one_title")
    two_title.to_csv("./data/odd_titles/two_title")
    three_title.to_csv("./data/odd_titles/three_title")
    four_title.to_csv("./data/odd_titles/four_title")

def null_analysis(df):

    # null titles
    null_ti = df[df['tokenized_title'].str.match("00000000", na=False)]
    null_ti_len = len(null_ti)
    null_ti_uid = list(null_ti['uid'])
    null_ti.to_csv("./data/odd_titles/null_ti")
    print(f"# of articles with null titles: {null_ti_len}")

    return null_ti_uid

def gone_analysis(df):

    # Page taken off
    gone_ar = df[df['content'].str.match(
        "the page you've requested has been moved or taken off the site we apologize for the inconvenience")]
    gone_ar_len = len(gone_ar)
    gone_ar_uid = list(gone_ar['uid'])
    gone_ar.to_csv("./data/odd_titles/gone_ar")
    print(f"# of page taken off: {gone_ar_len}")

    return gone_ar_uid

def fb_analysis(df):

    # Restricted articles (one)
    restricted_ar = df[df['content'].str.match('e mail screen name password confirm password please type the code by clicking register')]
    restricted_ar_len = len(restricted_ar)
    restricted_ar_uid = list(restricted_ar['uid'])
    restricted_ar.to_csv("./data/odd_titles/restricted_ar")
    print(f"# of fb restricted articles: {restricted_ar_len}")

    return restricted_ar_uid

def goo_analysis(df):

    # Google log in
    go_restricted_ar = df[df['content'].str.match('one account all of google sign in to continue to google+')]
    go_restricted_ar_len = len(go_restricted_ar)
    go_restricted_ar_uid = list(go_restricted_ar['uid'])
    go_restricted_ar.to_csv("./data/odd_titles/go_restricted_ar")
    print(f"# of google restricted articles: {go_restricted_ar_len}")

    return go_restricted_ar_uid

def non_hapaxes_analysis(df):

    # Generate non-hapaxes
    hapaxes = nltk.FreqDist(conc_titles).hapaxes()
    non_hapaxes = list(set(conc_titles).difference(set(hapaxes)))

    # fp = open("./data/odd_titles/hapaxes_title_ana.txt", "w")
    # for item in hapaxes:
    #     fp.write("%s\n" % item)
    # fp.close()
    # fp = open("./data/odd_titles/nonhapaxes_title_ana.txt", "w")
    # for item in non_hapaxes:
    #     fp.write("%s\n" % item)
    # fp.close()

    non_unique_ti = df[df['concatenated'].isin(non_hapaxes)]
    non_unique_ti_len = len(non_unique_ti)
    non_unique_ti_uid = list(non_unique_ti['uid'])
    non_unique_ti.to_csv("./data/odd_titles/non_hapaxes")

    # Adding Frequency Condition
    d_hap_freq = collections.defaultdict(int)
    for i in non_unique_ti['concatenated']:
        d_hap_freq[i] += 1

    ti_two_times, len_two = [], 0
    ti_three_times, len_three = [], 0
    ti_four_times, len_four = [], 0
    ti_multi_times, len_multi = [], 0
    freq_list = []
    for j in d_hap_freq:
        if d_hap_freq[j] == 2:
            ti_two_times.append((j, 2))
            len_two += 2
            freq_list.append(2)
        elif d_hap_freq[j] == 3:
            ti_three_times.append((j, 3))
            len_three += 3
            freq_list.append(3)
        elif d_hap_freq[j] == 4:
            ti_four_times.append((j, 4))
            len_four += 4
            freq_list.append(4)
        elif d_hap_freq[j] > 4:
            ti_multi_times.append((j, d_hap_freq[j]))
            len_multi += d_hap_freq[j]
            freq_list.append(d_hap_freq[j])
    print(f"There are {len_two} two times, {len_three} three times, {len_four} four, and {len_multi} multi non-hapaxe titles ")

    # Saving Odd Titled Articles
    # fp = open("./data/odd_titles/ti_two_times.txt", "w")
    # fp.write('\n'.join('%s %i' % x for x in ti_two_times))
    # fp.close()
    #
    # fp = open("./data/odd_titles/ti_three_times.txt", "w")
    # fp.write('\n'.join('%s %i' % x for x in ti_three_times))
    # fp.close()
    #
    # fp = open("./data/odd_titles/ti_four_times.txt", "w")
    # fp.write('\n'.join('%s %i' % x for x in ti_four_times))
    # fp.close()
    #
    # fp = open("./data/odd_titles/ti_multi_times.txt", "w")
    # fp.write('\n'.join('%s %i' % x for x in ti_multi_times))
    # fp.close()

    # Plotting frequency
    # print(freq_list)
    # bins = [0, 2, 4, 6, 8, 10, 20, 30, 50]
    # plt.hist(freq_list, bins, histtype='bar', range=(2, 50), rwidth=0.5, color='g')
    # plt.xlabel("frequency of title")
    # plt.ylabel("count")
    # plt.title("distribution of title frequency")
    # plt.grid(True)
    # plt.show()

if __name__ == "__main__":

    conc_titles, all = pandas_df(X)
    df = pd.DataFrame(all, columns=['uid', 'tokenized_title', 'concatenated', 'len_title', 'content'])

    len_analysis(df)
    null_analysis_uid = null_analysis(df)
    gone_ar_uid = gone_analysis(df)
    restricted_ar_uid = fb_analysis(df)
    go_restricted_ar_uid = goo_analysis(df)
    # non_hapaxes_analysis(df)

    test_odd = null_analysis_uid + gone_ar_uid + restricted_ar_uid + go_restricted_ar_uid
    print(f"test {len(test_odd)}")
    odd_ti = list(set(null_analysis_uid + gone_ar_uid + restricted_ar_uid + go_restricted_ar_uid))
    print(f"final {len(odd_ti)}")
    print(odd_ti)

    pickle_out = open("./data/odd_titles.pkl", "wb")
    pickle.dump(odd_ti, pickle_out)
    pickle_out.close()

