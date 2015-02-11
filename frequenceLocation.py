__author__ = 'aladdin'
import math
import scipy.io
import numpy as np
import pickle

data = scipy.io.loadmat('/home/aladdin/Dropbox/finalShenzhen9386V6.mat')
mylong = data.get('long')
mylat = data.get('lat')

thresCom = 1e-8
time = len(mylong)
datasize = len(mylong[0])


theta = 1.1 * math.cos(mylat[0][0]*math.pi/180)
index = []
for i in range(time):
    print i
    if i==0:
        index.append([x for x in range(datasize)])
        continue
    else:
        index.append([x for x in index[i-1]])

    for j in range(datasize):
        for k in range(j+1,datasize):
            tmpj = index[i-1][j]
            tmpk = index[i-1][k]
            if math.pow((mylong[i][tmpj]-mylong[i][tmpk])*1.1,2) + math.pow((mylat[i][tmpj]-mylat[i][tmpk])*theta,2) <= thresCom:
                if np.random.random() < 0.5:
                  #  print j,k
                    (index[i][j], index[i][k]) = (index[i][k], index[i][j])
    print index[i]
for i in range(len(index)):
    print index[i ]

filename = open('myrandomindex2.txt', 'w')
pickle.dump(index, filename)
filename.close()