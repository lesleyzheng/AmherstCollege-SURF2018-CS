import pickle
import sys

#prints out the highest percents and their corrospongind words pairs for real and fake articles where a percent is the percentage that a pair of words appear together in the articles

if __name__ == '__main__':
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    pickle_in = open(f'./data/{filename}', 'rb')
    (matrix1, list_words1), desc = pickle.load(pickle_in)
    p_in = open(f'./data/{filename2}', 'rb')
    (matrix2, list_words2), desc2 = pickle.load(p_in)



    high_percents = []
    those_words = []
    for i in range(len(matrix1)):
        for j in range(i + 1, len(matrix1[0])):
            if matrix1[i][j] > 70:
                high_percents.append(matrix1[i][j])
                those_words.append((list_words1[i], list_words1[j]))

    print(high_percents)
    print(those_words)

    print('now ones')

    high_percents2 = []
    those_words2 = []
    for i in range(len(matrix2)):
        for j in range(i + 1, len(matrix2[0])):
            if matrix2[i][j] > 70:
                high_percents2.append(matrix2[i][j])
                those_words2.append((list_words2[i], list_words2[j]))

    print(high_percents2)
    print(those_words2)










