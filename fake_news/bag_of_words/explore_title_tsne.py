import pickle
import matplotlib.pyplot as plt

#program for identifying articles from graphs
pickle_in = open("./data/title_tsne_experiment.pkl", 'rb')
matrix, Y = pickle.load(pickle_in)
pickle_in.close()

red_clump = []

for i in range(len(matrix)):
    if matrix[i][0] > -63 and matrix[i][0] < -59 and matrix[i][1] > 22 and matrix[i][1] < 26:
        print(f"A: index {i} has a value of {matrix[i]}, in the clump from [-59 to -63], [22 to 26]")
    if matrix[i][0] > -68 and matrix[i][0] < -66.5 and matrix[i][1] > -38.75 and matrix[i][1] < -37.5:
        print(f"B: index {i} has a value of {matrix[i]}, in the clump from [-66.5 to -68], [-37.5 to -38.75]")
    if matrix[i][0] > -72 and matrix[i][0] < -68 and matrix[i][1] > 6 and matrix[i][1] < 10:
        print(f"index {i} has a value of {matrix[i]}, in the clump from [-68 to -72], [6 to 10]")
    if matrix[i][0] > -59 and matrix[i][0] < -45 and matrix[i][1] > -34 and matrix[i][1] < -21:
        print(f"C: index {i} has a value of {matrix[i]}, in the clump from [-45 to -59], [-21 to -34]")
        print(f"and my truth value is {Y[i][2]}")
        if Y[i][2] == 0:
            red_clump.append(i)
    if matrix[i][0] > -34 and matrix[i][0] < -27 and matrix[i][1] > -16 and matrix[i][1] < -8:
        print(f"C: index {i} has a value of {matrix[i]}, in the clump from [-27 to -34], [-8 to -16]")
        print(f"and my truth value is {Y[i][2]}")

print(red_clump)
targets = [0,1]
colors = ['r', 'b']
for target, color in zip(targets,colors):
    inds_to_keep = []
    for i in range(len(Y)):
        if Y[i][2] == target:
            inds_to_keep.append(i)
    plt.scatter(matrix[inds_to_keep, 0], matrix[inds_to_keep, 1], alpha = 0.3,
            c = color, s = 20)
print("computed")
plt.xlabel('component 1')
plt.ylabel('component 2')

plt.show()