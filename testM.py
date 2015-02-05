__author__ = 'aladdin'
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from mReader import homotopypath

filename = open('shenzhen3.txt')
m = homotopypath()
m = pickle.load(filename)
filename.close()
print('here')
fig = plt.figure(1)
m.drawTra2([4, 8])
plt.show()

m.drawTra2([3, 29])

