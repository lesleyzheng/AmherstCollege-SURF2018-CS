import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import sys
from matrix_reduction_randomization import reduc_rand

if __name__ == "__main__":

    import_file = str(sys.argv[1])
    reduction_status = int(sys.argv[2]) # 0 for don't rand reduce; 1 for rand reduce
    reduction_size = int(sys.argv[3])
    reduced_filename = str(sys.argv[4])

    # load data
    matrix_in = open(f'./data/{import_file}', 'rb')
    (matrix, uids), description = pickle.load(matrix_in)
    # need to change depending on import type
    # pickle.dump(((matrix, uid), description), pickle_out)
    matrix_in.close()

    if reduction_status == 1:
        reduc_rand(matrix, reduction_size, reduced_filename)
        new_matrix_in = open(f'./data/', 'rb')
        (matrix, uids, labels), desc = pickle.load(new_matrix_in) # WARNING: labels don't match!
        new_matrix_in.close()

    # labels
    # finn = "./data/FakeNewsData.pkl"
    # fin = open(finn, "rb")
    # (X, Y), des = pickle.load(fin)
    # fin.close()
    # print(des)
    # labels = [None]*len(uids)
    # print(len(matrix)==len(uids))
    # for index in range(len(matrix)):
    #     for i in range(len(Y)):
    #         if uids[index] == Y[i][1]:
    #             labels[index] = Y[i][2]
    #             break

    # standardization
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix = scaler.transform(matrix)

    # pca
    pca = PCA(n_components=100)
    pca.fit(matrix)
    matrix_pca = pca.transform(matrix)

    # outliers
    # iso_f = IsolationForest(contamination = 0.05, random_state = 42)
    # iso_f.fit(matrix_pca)
    # preds = iso_f.predict(matrix_pca)

    # dump plotting information
    print(len(matrix_pca))
    pickle_out = open('./data/matrixv2_pca_plot.pkl', 'wb')
    pickle.dump(((matrix_pca, uids), "pca matrix 100 dimensions for matrixv2"), pickle_out)
    pickle_out.close()