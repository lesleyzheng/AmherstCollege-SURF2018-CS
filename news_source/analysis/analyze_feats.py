import pickle
import sys

#prints out the top n features after feature selection has been performed
def look(feat_list, oed, n):

    names = [i for i in oed]

    sort_list = sorted(zip(map(lambda x: round(x, 4), feat_list), names), reverse=True)

    for i in range(n):
        print(sort_list[i])



if __name__ == '__main__':
    file_path = sys.argv[1]  #the path to the feature list
    dict_path = sys.argv[2] #path to the 10,000 list
    num = int(sys.argv[3]) #number of features to print


    pickle_in = open(file_path, "rb")
    (list_feats, desc) = pickle.load(pickle_in)


    pickle_in2 = open(dict_path, 'rb')
    top_10k = pickle.load(pickle_in2)

    look(list_feats, top_10k, num)
