import pickle
from collections import defaultdict
from sklearn.preprocessing import StandardScaler
import sys

#makes a matrix where each row is an article and each column is one of the 52 features we hand selected
def getUIDs(counts):
    uids = [None] * len(counts)
    for i in range(len(counts)):
        uids[i] = counts[i][0]
    return uids

def getCountsMatrix(counts):


    dict = defaultdict(int, {'CC': 0, 'CD': 0,'DT': 0,
                             'EX': 0,'FW': 0,'IN': 0,'JJ': 0,
                             'JJR': 0,'JJS': 0,'LS': 0,'MD': 0,
                             'NN': 0,'NNS': 0,'NNP': 0,'NNPS': 0,
                             'PDT': 0,'POS': 0,'PRP': 0,'PRP$': 0,
                             'RB': 0,'RBR': 0,'RBS': 0,'RP': 0,
                             'TO': 0,'UH': 0,'VB': 0,'VBD': 0,
                             'VBG': 0,'VBN': 0,'VBP': 0,'VBZ': 0,
                             'WDT': 0,'WP': 0,'WP$': 0,'WRB': 0,
                             'PLACES': 0, 'PEOPLE': 0,'ORGS': 0,
                             'MONEY':0,'PERCENTS': 0,'DATES': 0,
                             'QUOTES': 0,'EXPLETIVES': 0})


    length = len(counts)
    newcounts = [None]*length

    for a in range(length):
        ind = 0
        temp = [None]*50
        for i in range(4):
            temp[i] = counts[a][i + 9]
            ind += 1
        # 0 = # of words
        # 1 = # of sentences
        # 2 = avg # of letters in words
        # 3 = avg # of words in sentences

        for k in dict:
            if k != 'QUOTES' and k != 'POS':
                temp[ind] = counts[a][13][k]
                ind += 1
        # 4-46: adds everything in default dict; if it has a value in the counts defaultdict, it adds that value, otherwise 0

        for i in range(5):
            temp[ind + i] = counts[a][14 + i]
        # 47 = # of ?
        # 48 = # of .
        # 49 = # of !
        # 50 = # of ,
        # 51 = compound sentiment

        newcounts[a] = temp

    return newcounts

def getTitleCountsMatrix(counts):

    dict = defaultdict(int, {'CC': 0, 'CD': 0,'DT': 0,
                             'EX': 0,'FW': 0,'IN': 0,
                             'JJ': 0,'JJR': 0,'JJS': 0,
                             'LS': 0,'MD': 0,'NN': 0,
                             'NNS': 0,'NNP': 0,'NNPS': 0,
                             'PDT': 0,'POS': 0,'PRP': 0,
                             'PRP$': 0,'RB': 0,'RBR': 0,
                             'RBS': 0,'RP': 0,'TO': 0,
                             'UH': 0,'VB': 0,'VBD': 0,
                             'VBG': 0,'VBN': 0,'VBP': 0,
                             'VBZ': 0,'WDT': 0,'WP': 0,
                             'WP$': 0,'WRB': 0, 'PLACES': 0,
                             'PEOPLE': 0,'ORGS': 0,'MONEY':0,
                             'PERCENTS': 0,'DATES': 0,'QUOTES': 0,
                             'EXPLETIVES': 0})


    length = len(counts)
    newcounts = [None]*length

    for a in range(length):
        ind = 0
        temp = [None]*50
        for i in range(2):
            temp[i] = counts[a][i + 1]
            ind += 1
        # 0 = # of words
        # 1 = avg # of letters in words
        if not isinstance(counts[a][3], float) and len(counts[a][3]) != 0:
            for k in dict:
                temp[ind] = counts[a][3][k]
                ind += 1
        else:
            for f in range(43):
                temp[ind] = 0
                ind += 1
        # 2-44: adds everything in default dict; if it has a value in the counts defaultdict, it adds that value, otherwise 0

        for i in range(5):
            #temp[ind + i] = counts[a][4 + i]
            temp[ind] = counts[a][4 + i]
            ind+=1
        # 45 = # of ?
        # 46 = # of .
        # 47 = # of !
        # 48 = # of ,
        # 49 = compound sentiment

        newcounts[a] = temp

    return newcounts

def scaleMatrix(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_s = scaler.transform(matrix)
    return matrix_s

def pickleCountsMatrix(matrix, uids, num, title = False, standard = False):
    if standard == False:
        if title == False:
            pickle_out = open("./data/{0}_matrix/{0}_flat_counts_content_clean2.pkl".format(num), 'wb')
            desc = "A matrix from our gathered news data containing 52 columns, where each row corresponds to an article and each column contains a numeric characteristic of that article"
        if title:
            pickle_out = open("./data/{0}_matrix/{0}_flat_counts_title.pkl".format(num), 'wb')
            desc = "A matrix from our gathered news data containing 50 columns, where each row corresponds to an article and each column contains a numeric characteristic of that article"
    if standard:
        if title == False:
            pickle_out = open("./data/{0}_matrix/{0}_scaled_counts_content_clean2.pkl".format(num), 'wb')
            desc = "A scaled and standardized matrix from our gathered data, ready for PCA/t-SNE/isomapping/etc. "
        if title:
            pickle_out = open("./data/{0}_matrix/{0}_scaled_counts_title.pkl".format(num), 'wb')
            desc = "A scaled and standardized matrix from our gathered data, ready for PCA/t-SNE/isomapping/etc. "

    pickle.dump(((matrix, uids), desc), pickle_out)
    pickle_out.close()


if __name__ == "__main__":
    filepath = str(sys.argv[1])
    num = int(sys.argv[2])
    pickle_in = open(filepath, "rb")
    counts, desc = pickle.load(pickle_in)

    content = getCountsMatrix(counts)
    # titles = getTitleCountsMatrix(counts)
    uids = getUIDs(counts)
    scaled_content = scaleMatrix(content)
    # scaled_titles = scaleMatrix(titles)
    # num = 3000

    pickleCountsMatrix(content, uids, num)
    # pickleCountsMatrix(titles, uids, num, title = True, standard=False)
    pickleCountsMatrix(scaled_content, uids,num, title = False, standard=True)
    # pickleCountsMatrix(scaled_titles, uids,num, title = True, standard=True)

    print("pickled")
