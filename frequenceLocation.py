__author__ = 'aladdin'
import math
import scipy.io
import numpy as np
data = scipy.io.loadmat('/mnt/new/matlab2012b/bin/finalShenzhen9386V6.mat')
mylong = data.get('long')
mylat = data.get('lat')

thresCom = 1e-8
time = len(mylong)
datasize =  len(mylong[0])


theta = 1.1 * math.cos(mylat[0][0]*math.pi/180)
index = []
for i in range(time):
    print i
    if i==0:
        index.append([x for x in range(datasize)])
    else:
        index.append(index[i-1])

    for j in range(datasize):
        for k in range(j+1,datasize):
            tmpj = index[i-1][j]
            tmpk = index[i-1][k]
            if math.pow((mylong[i][tmpj]-mylong[i][tmpk])*1.1,2) + math.pow((mylat[i][tmpj]-mylat[i][tmpk])*theta,2) <= thresCom:
                if np.random.random() < 0.5:
                    (index[i][j], index[i][k]) = (index[i][k], index[i][j])
print index