import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from collections import defaultdict



#runs various methods to explore the values in the counts matrix
def getXLab(i):
    if i == 0:
        return "Number of Words"
    if i == 1:
        return "Number of Sentences"
    if i == 2:
        return "Average Number of Letters per Word"
    if i == 3:
        return "Average Number of Words per Sentence"
    if i == 4:
        return "Number of Coordinating Conjunctions (CC)"
    if i == 5:
        return "Number of Cardinal Digits (CD)"
    if i == 6:
        return "Number of Determiners (DT)"
    if i == 7:
        return "Number of Existential theres (EX)"
    if i == 8:
        return "Number of Foreign Words (FW)"
    if i == 9:
        return "Number of Prepositions (IN)"
    if i == 10:
        return "Number of Adjectives (JJ)"
    if i == 11:
        return "Number of Comparative Adjectives (JJR)"
    if i == 12:
        return "Number of Superlative Adjectives (JJS)"
    if i == 13:
        return "Number of List Markers (LS)"
    if i == 14:
        return "Number of Modals (MD)"
    if i == 15:
        return "Number of Singular Nouns (NN)"
    if i == 16:
        return "Number of Plural Nouns (NNS)"
    if i == 17:
        return "Number of Singular Proper Nouns (NNP)"
    if i == 18:
        return "Number of Plural Proper Nouns (NNPS)"
    if i == 19:
        return "Number of Predeterminers (PDT)"
    if i == 20:
        return "Number of Possessive Endings (POS)"
    if i == 21:
        return "Number of Personal Pronouns (PRP)"
    if i == 22:
        return "Number of Possessive Pronouns (PRP$)"
    if i == 23:
        return "Number of Adverbs (RB)"
    if i == 24:
        return "Number of Comparative Adverbs (RBR)"
    if i == 25:
        return "Number of Superlative Adverbs (RBS)"
    if i == 26:
        return "Number of Particles (RP)"
    if i == 27:
        return "Number of Unconjugated Verbs (eg. 'to go') (TO)"
    if i == 28:
        return "Number of Interjections (UH)"
    if i == 29:
        return "Number of Verbs, Base Form (VB)"
    if i == 30:
        return "Number of Verbs, Past Tense (VBD)"
    if i == 31:
        return "Number of Verbs, Gerund/Present Participle (VBG)"
    if i == 32:
        return "Number of Verbs, Past Participle (VBN)"
    if i == 33:
        return "Number of Verbs, Singular Present (VBP)"
    if i == 34:
        return "Number of Verbs, 3rd Person Singular Present (VBZ)"
    if i == 35:
        return "Number of Wh-Determiners (WDT)"
    if i == 36:
        return "Number of Wh-Pronouns (WP)"
    if i == 37:
        return "Number of Possessive Wh-Pronouns (WP$)"
    if i == 38:
        return "Number of Wh-Adverbs (WRB)"
    if i == 39:
        return "Number of Places"
    if i == 40:
        return "Number of People"
    if i == 41:
        return "Number of Organizations"
    if i == 42:
        return "Number of References to Money"
    if i == 43:
        return "Number of References to Percents"
    if i == 44:
        return "Number of Dates"
    if i == 45:
        return "Number of Quotations"
    if i == 46:
        return "Number of Expletives"
    if i == 47:
        return "Number of Question Marks"
    if i == 48:
        return "Number of Periods"
    if i == 49:
        return "Number of Exclamation Points!"
    if i == 50:
        return "Number of Commas"
    if i == 51:
        return "Compound Sentiment"

def getXTitleLab(i):
    if i == 0:
        return "Number of Words"
    if i == 1:
        return "Average Number of Letters per Word"
    if i == 2:
        return "Number of Coordinating Conjunctions (CC)"
    if i == 3:
        return "Number of Cardinal Digits (CD)"
    if i == 4:
        return "Number of Determiners (DT)"
    if i == 5:
        return "Number of Existential theres (EX)"
    if i == 6:
        return "Number of Foreign Words (FW)"
    if i == 7:
        return "Number of Prepositions (IN)"
    if i == 8:
        return "Number of Adjectives (JJ)"
    if i == 9:
        return "Number of Comparative Adjectives (JJR)"
    if i == 10:
        return "Number of Superlative Adjectives (JJS)"
    if i == 11:
        return "Number of List Markers (LS)"
    if i == 12:
        return "Number of Modals (MD)"
    if i == 13:
        return "Number of Singular Nouns (NN)"
    if i == 14:
        return "Number of Plural Nouns (NNS)"
    if i == 15:
        return "Number of Singular Proper Nouns (NNP)"
    if i == 16:
        return "Number of Plural Proper Nouns (NNPS)"
    if i == 17:
        return "Number of Predeterminers (PDT)"
    if i == 18:
        return "Number of Possessive Endings (POS)"
    if i == 19:
        return "Number of Personal Pronouns (PRP)"
    if i == 20:
        return "Number of Possessive Pronouns (PRP$)"
    if i == 21:
        return "Number of Adverbs (RB)"
    if i == 22:
        return "Number of Comparative Adverbs (RBR)"
    if i == 23:
        return "Number of Superlative Adverbs (RBS)"
    if i == 24:
        return "Number of Particles (RP)"
    if i == 25:
        return "Number of Unconjugated Verbs (eg. 'to go') (TO)"
    if i == 26:
        return "Number of Interjections (UH)"
    if i == 27:
        return "Number of Verbs, Base Form (VB)"
    if i == 28:
        return "Number of Verbs, Past Tense (VBD)"
    if i == 29:
        return "Number of Verbs, Gerund/Present Participle (VBG)"
    if i == 30:
        return "Number of Verbs, Past Participle (VBN)"
    if i == 31:
        return "Number of Verbs, Singular Present (VBP)"
    if i == 32:
        return "Number of Verbs, 3rd Person Singular Present (VBZ)"
    if i == 33:
        return "Number of Wh-Determiners (WDT)"
    if i == 34:
        return "Number of Wh-Pronouns (WP)"
    if i == 35:
        return "Number of Possessive Wh-Pronouns (WP$)"
    if i == 36:
        return "Number of Wh-Adverbs (WRB)"
    if i == 37:
        return "Number of Places"
    if i == 38:
        return "Number of People"
    if i == 39:
        return "Number of Organizations"
    if i == 40:
        return "Number of References to Money"
    if i == 41:
        return "Number of References to Percents"
    if i == 42:
        return "Number of Dates"
    if i == 43:
        return "Number of Quotations"
    if i == 44:
        return "Number of Expletives"
    if i == 45:
        return "Number of Question Marks"
    if i == 46:
        return "Number of Periods"
    if i == 47:
        return "Number of Exclamation Points!"
    if i == 48:
        return "Number of Commas"
    if i == 49:
        return "Compound Sentiment"



def showNumOf(matrix, i, content):
    plt.hist(matrix[:, i], 50)
    if content:
        plt.xlabel(getXLab(i))
        plt.ylabel("Number of Articles")
        plt.title(f"Distribution of {getXLab(i)} for all Article Bodies")
        plt.savefig(f'./figs/contents_{i}.png')
    else:
        plt.xlabel(getXTitleLab(i))
        plt.ylabel("Number of Titles")
        plt.title(f"Distribution of {getXTitleLab(i)} for all Article Titles")
        plt.savefig(f'./figs/titles_{i}.png')

    plt.show()

def plotWithoutOutliers(matrix, i, content):
    lows, highs, superhighs = findOutliers(matrix, i, content)
    outliers = lows + highs + superhighs
    inds_to_keep = []
    for n in range(len(matrix)):
        if n not in outliers:
            inds_to_keep.append(n)
    inds_to_keep = np.array(inds_to_keep)
    matrix = matrix[inds_to_keep]
    showNumOf(matrix, i, content)

def findOutliers(matrix, i, content):
    i_col = [None] * len(matrix)
    for n in range(len(matrix)):
        i_col[n] = matrix[n][i]

    i_col.sort()
    q1 = np.percentile(i_col, 25)
    q3 = np.percentile(i_col, 75)
    iqr = q3-q1
    low_outlier = q1 - 1.5*iqr
    high_outlier = q3 + 1.5*iqr
    extra_high = q3 + 3*iqr

    lows, highs, superhighs = [], [], []
    for n in range(len(matrix)):
        if matrix[n][i] < low_outlier:
            lows.append(n)
        if matrix[n][i] > high_outlier:
            highs.append(n)
        if matrix[n][i] > extra_high:
            superhighs.append(n)

    if content == True:
        lab = getXLab(i)
    else:
        lab = getXTitleLab(i)
    print(f" ===================== COLUMN {i} ===================== ")
    print(f"min value for column {i} = {lab} is {np.min(i_col)}")
    print(f"q1 value for column {i} = {lab} is {q1}")
    print(f"median value for column {i} = {lab} is {np.median(i_col)}")
    print(f"q3 value for column {i} = {lab} is {q3}")
    print(f"max value for column {i} = {lab} is {np.max(i_col)}")

    print(f"Low outlier for column {i} = {lab} is {low_outlier}")
    print(f"There are {len(lows)} low outliers")
    print(f"High outlier for column {i} = {lab} is {high_outlier}")
    print(f"There are {len(highs)} high outliers")
    print(f"Extreme high outlier for column {i} = {lab} is {extra_high}")
    print(f"There are {len(superhighs)} high outliers")

    return (lows, highs, superhighs)


def findRepeats(all, set, nums):
    ones = []
    twos = []
    threes = []
    fours = []
    fives = []
    tens = []
    fifteens = []
    twenties = []
    for i in set:
        c = all.count(i)
        if c > nums[0]:
            ones.append(i)
        if c > nums[1]:
            twos.append(i)
        if c > nums[2]:
            threes.append(i)
        if c > nums[3]:
            fours.append(i)
        if c > nums[4]:
            fives.append(i)
        if c > nums[5]:
            tens.append(i)
        if c > nums[6]:
            fifteens.append(i)
        if c > nums[7]:
            twenties.append(i)

    print(f"================== COUNT > {nums[0]} =================")
    print(f" repeats for count > {nums[0]} = ", len(ones))
    print(ones)

    print(f"================== COUNT > {nums[1]} =================")
    print(f" repeats for count > {nums[1]} = ", len(twos))
    print(twos)

    print(f"================== COUNT > {nums[2]} =================")
    print(f" repeats for count > {nums[2]} = ", len(threes))
    print(threes)

    print(f"================== COUNT > {nums[3]} =================")
    print(f" repeats for count > {nums[3]} = ", len(fours))
    print(fours)

    print(f"================== COUNT > {nums[4]} =================")
    print(f" repeats for count > {nums[4]} = ", len(fives))
    print(fives)

    print(f"================== COUNT > {nums[5]} =================")
    print(f" repeats for count > {nums[5]} = ", len(tens))
    print(tens)

    print(f"================== COUNT > {nums[6]} =================")
    print(f" repeats for count > {nums[6]} = ", len(fifteens))
    print(fifteens)

    print(f"================== COUNT > {nums[7]} =================")
    print(f" repeats for count > {nums[7]} = ", len(twenties))
    print(twenties)


def printIDs(ids, matrix, X, Y):
    for i in ids:
        print("=========================================")
        print(f"index {i}")
        print(matrix[i][0])
        print(X[i][2])
        # print(X[i][3])
        print(Y[i][2])
        print(X[i][1])
        # print(Y[i][1])


def doContentStuff():
    pickle_in = open('./data/flat_counts_content.pkl', 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    pickle_in.close()
    print(desc)
    matrix = np.array(matrix)
    print(type(matrix))

    pickle_in1 = open('./data/FakeNewsData.pkl', 'rb')
    (X, Y), desc1 = pickle.load(pickle_in1)
    pickle_in1.close()

    all_lows = []
    lows_list, highs_list, super_list = [], [], []
    all_highs = []
    all_superhighs = []
    for i in range(len(matrix[0])):
        showNumOf(matrix, i, True)
        L, H, S = findOutliers(matrix, i, True)
        lows_list.append(L)
        highs_list.append(H)
        super_list.append(S)
        for l in range(len(L)):
            all_lows.append(L[l])
        for h in range(len(H)):
            all_highs.append(H[h])
        for s in range(len(S)):
            all_superhighs.append(S[s])

    print(all_lows)
    print("lows = ", len(all_lows))
    print("highs = ", len(all_highs))
    print("extremes = ", len(all_superhighs))

    print("set of all lows = ", len(list(set(all_lows))))
    print("set of all highs = ", len(list(set(all_highs))))
    print("set of all extremes = ", len(list(set(all_superhighs))))
    lows = list(set(all_lows))
    highs = list(set(all_highs))
    superhighs = list(set(all_superhighs))
    superhighs.sort()
    print(superhighs)
    print(len(superhighs))

    #
    # nums = [1,2,3,4,5,10,15,20]
    #
    # print("=*=*=*=*=*=*=*=*=*=*=*=*=* LOWS =*=*=*=*=*=*=*=*=*=*=*=*=*")
    #
    # repeat_lows1 = findRepeats(all_lows, lows, nums)
    #
    # print("=*=*=*=*=*=*=*=*=*=*=*=*=* HIGHS =*=*=*=*=*=*=*=*=*=*=*=*=*")
    #
    # repeat_highs1 = findRepeats(all_highs, highs, nums)
    #
    # print("=*=*=*=*=*=*=*=*=*=*=*=*=* EXTREMES =*=*=*=*=*=*=*=*=*=*=*=*=*")
    #
    # repeat_supers1 = findRepeats(all_superhighs, superhighs, nums)
    #
    # # print("=*=*=*=*=*=*=*=*=*=*=*=*=* EXTREMES =*=*=*=*=*=*=*=*=*=*=*=*=*")
    #
    # # bignums = [25, 30, 35, 40, 45, 50, 52, 55]
    #
    # # findRepeats(all_superhighs, superhighs, bignums)
    #
    # # extremes45 = [1204, 2634, 10902, 13331, 15726, 18914, 22230,
    # #               22235, 24378, 27264, 27786, 29594, 34587, 34638,
    # #               39376, 39748, 39777, 43381, 45245, 47604, 50641,
    # #               50688, 53062, 55504, 59919, 60615, 63968, 65271,
    # #               65584, 65606, 70265, 70592, 77196, 81418, 81434,
    # #               86173, 90773, 91218, 91239, 95635, 96035, 97579,
    # #               99156, 99158, 99166, 100588, 100893, 100906, 111419,
    # #               111430, 115834, 116112, 116148, 120645, 121092,
    # #               122657, 125492, 125599, 126042, 126093]
    # #
    # # printIDs(extremes45, matrix, X, Y)


def doTitleStuff():
    pickle_in = open('./data/flat_counts_title.pkl', 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    pickle_in.close()
    print(desc)
    matrix = np.array(matrix)


    pickle_in1 = open('./data/FakeNewsData.pkl', 'rb')
    (X, Y), desc1 = pickle.load(pickle_in1)
    pickle_in1.close()

    all_lows = []
    lows_list, highs_list, super_list = [], [], []
    all_highs = []
    all_superhighs = []
    for i in range(len(matrix[0])):
        showNumOf(matrix, i, False)
        L, H, S = findOutliers(matrix, i, False)
        lows_list.append(L)
        highs_list.append(H)
        super_list.append(S)
        for l in range(len(L)):
            all_lows.append(L[l])
        for h in range(len(H)):
            all_highs.append(H[h])
        for s in range(len(S)):
            all_superhighs.append(S[s])

    lows = list(set(all_lows))
    highs = list(set(all_highs))
    superhighs = list(set(all_superhighs))

    print("lows = ", len(all_lows))
    print("highs = ", len(all_highs))
    print("extremes = ", len(all_superhighs))

    print("set of lows = ", len(lows))
    print("set of highs = ", len(highs))
    print("set of extremes = ", len(superhighs))

    # nums = [1, 2, 3, 4, 5, 10, 15, 20]
    #
    # # print("=*=*=*=*=*=*=*=*=*=*=*=*=* LOWS =*=*=*=*=*=*=*=*=*=*=*=*=*")
    # #
    # # repeat_lows1 = findRepeats(all_lows, lows, nums)
    # #
    # # print("=*=*=*=*=*=*=*=*=*=*=*=*=* HIGHS =*=*=*=*=*=*=*=*=*=*=*=*=*")
    # #
    # # repeat_highs1 = findRepeats(all_highs, highs, nums)
    # #
    # # print("=*=*=*=*=*=*=*=*=*=*=*=*=* EXTREMES =*=*=*=*=*=*=*=*=*=*=*=*=*")
    # #
    # # repeat_supers1 = findRepeats(all_superhighs, superhighs, nums)
    #
    # highs_15 = [24100, 24101, 34968, 34985, 37636, 37637, 49586,
    #             49591, 49592, 49594, 49595, 49633,50935, 58373,
    #             58380, 62338, 64410, 64434, 64442, 77793, 78759]
    #
    # extremes_10 = [7214, 8751, 11169, 11183, 11202, 14336, 15932,
    #             24100, 24101, 26066, 26769, 29937, 29980, 30539,
    #                30923, 34967, 34968, 34985, 34992, 36569, 36573,
    #                37435, 37636, 37637, 38594, 38604, 38608, 40087,
    #                40092, 40095, 40317, 41558, 43149, 44645, 49586,
    #                49591, 49592, 49594, 49595, 49633, 50935, 58373,
    #                58380, 59265, 59269, 59278, 59299, 59477, 60910,
    #                60925, 62338, 62471, 62478, 63582, 63584, 64410,
    #                64434, 64442, 64443, 64579, 65962, 67513, 70909,
    #                77008, 77793, 77800, 78759, 79325, 81423, 82908,
    #                83198, 86428, 86446, 87642, 88015, 88040, 89908,
    #                92677, 92918, 92926, 92967, 93196, 94014, 94026,
    #                94034, 94907, 96322, 104379, 104798, 104959,
    #                104981, 104984, 105000, 106469, 106569, 107147,
    #                108819, 108824, 110329, 111714, 113096, 113123,
    #                115080, 115229, 116121, 117741, 118005, 118380,
    #                118729, 118752, 120822, 124112, 124903, 126075,
    #                129265, 129274, 129283, 129285]
    #
    # printIDs(highs_15, matrix, X, Y)
def ContentOutliers():
    pickle_in = open('./data/flat_counts_content.pkl', 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    pickle_in.close()
    print(desc)
    matrix = np.array(matrix)

    for i in range(len(matrix[0])):
        plotWithoutOutliers(matrix, i, True)

def TitleOutliers():
    pickle_in = open('./data/flat_counts_title.pkl', 'rb')
    (matrix, ids), desc = pickle.load(pickle_in)
    pickle_in.close()
    print(desc)
    matrix = np.array(matrix)

    for i in range(len(matrix[0])):
        plotWithoutOutliers(matrix, i, False)

if __name__ == '__main__':
  TitleOutliers()