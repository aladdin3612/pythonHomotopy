__author__ = 'aladdin'
import math
import scipy.io
import numpy as np
import pickle


def ccw(A, B, C):
    """Tests whether the turn formed by A, B, and C is ccw"""
    return (B[0]- A[0]) * (C[1] - A[1]) > (B[1] - A[1]) * (C[0] - A[0])

def intersect(a1, b1, a2, b2):
    """Returns True if line segments a1b1 and a2b2 intersect."""
    return ccw(a1, b1, a2) != ccw(a1, b1, b2) and ccw(a2, b2, a1) != ccw(a2, b2, b1)


data = scipy.io.loadmat('/home/aladdin/Dropbox/finalShenzhen9386V6.mat')
mylong = data.get('long')
mylat = data.get('lat')

thresCom = 2.5e-9
time = len(mylong)
datasize = len(mylong[0])


theta = 1.1 * math.cos(mylat[0][0]*math.pi/180)
index = []


for i in range(time):
    print i
    total = 0
    if i==0:
        index.append([x for x in range(datasize)])
        continue
    else:
        index.append([x for x in index[i-1]])

    for j in range(datasize):
        tmpj = index[i-1][j]

        for k in range(j+1, datasize):
            tmpk = index[i-1][k]
            if intersect([mylong[i][tmpj], mylat[i][tmpj]], [mylong[i-1][tmpj], mylat[i-1][tmpj]], \
                [mylong[i][tmpk], mylat[i][tmpk]], [mylong[i-1][tmpk], mylat[i-1][tmpk]]):

                total += 1
                if np.random.random() < 0.5:
                  #  print j,k
                    (index[i][j], index[i][k]) = (index[i][k], index[i][j])
    print index[i]
    print total
for i in range(len(index)):
    print index[i]



filename = open('myrandomindex3.txt', 'w')
pickle.dump(index, filename)
filename.close()