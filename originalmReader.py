__author__ = 'aladdin'
__author__ = ' aladdin'
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import pickle
import random


class homotopypath():
    def __init__(self):
        self.G = nx.Graph()
        self.x = []
        self.y = []
        self.path = []
        self.trajectory = []
        self.integral = []
        self.inner = nx.Graph()
        self.innerpath = []


    def readpoly(self, fname):
        fin = open(fname)
        line = fin.readline()

        l = line.split()
        n = int(l[0])

        for i in range(n):
            line = fin.readline()
            l = line.split()
            self.inner.add_node(int(l[0]), x=float(l[1]), y=float(l[2]))

        fin.readline()
        line = fin.readline()
        l = line.split()
        n = int(l[0])
        counter = 0
        flag = 0
        for i in range(n):
            line = fin.readline()
            l = line.split()
            self.inner.add_edge(int(l[1]), int(l[2]))
            if flag == 0:
                self.innerpath.append([int(l[1]), int(l[2])])
                flag = 1
            else:
                l1 = int(l[1])
                l2 = int(l[2])
                if l1 < l2:
                    self.innerpath[counter].append(l2)
                else:
                    flag = 0
                    counter += 1
        print(self.innerpath)



        fin.close()


    def readfile(self, fname):
        fin = open(fname)

        line = " "

        while line != "":
            line = fin.readline()
            if line == "" or line[0] == "#":   # ignore the commment part
                continue

            l = line.split()
            if l[0] == "Vertex":
                self.G.add_node(int(l[1]), x=float(l[2]), y=float(l[3]), z=float(l[4]))

            if l[0] == "Face":
                self.G.add_edge(int(l[2]), int(l[3]))
                self.G.add_edge(int(l[3]), int(l[4]))
                self.G.add_edge(int(l[4]), int(l[2]))

            if l[0] == "Edge":
                continue

    def readdv(self, dvname):
        fin = open(dvname)

        line = " "

        while line != "":
            line = fin.readline()
            if line == "" or line[0] == "#":   # ignore the commment part
                continue

            l = line.split()
            if l[0] == "Vertex":
                continue

            elif l[0] == "Face":
                continue

            elif l[0] == "Edge":
                v1 = int(l[1])
                v2 = int(l[2])
                weight = float(l[3][l[3].find('(')+1:l[3].find(')')])
                if v1 > v2:
                    (v1, v2) = (v2, v1)
                    weight = -weight

                self.G.add_edge(v1, v2, w=weight)

     #           for e in self.G.edges_iter():
      #              print('%d, %d, %.5f' % (e[0],e[1],self.G.edge[e[0]][e[1]]['w']))



    def draw(self):
        for n in self.G.nodes_iter():
            plt.plot(self.G.node[n]['x'], self.G.node[n]['y'], 'b.', linewidth=3)

        for e in self.G.edges_iter():
            p1x = self.G.node[e[0]]['x']
            p1y = self.G.node[e[0]]['y']
            p2x = self.G.node[e[1]]['x']
            p2y = self.G.node[e[1]]['y']
            plt.plot([p1x, p2x], [p1y, p2y], c='r', linewidth=1)

        plt.show()

    def readtra(self, traname):
        fin = open(traname)

        line = fin.readline()
        l = line.split()
        n = int(l[0])

        for i in range(n):
            line = fin.readline()
            l = line.split()
            self.x.append([])
            self.y.append([])



            for j in range(int(l[0])):
                line = fin.readline()
                l = line.split()
                self.x[i].append(float(l[0]))
                self.y[i].append(float(l[1]))

    def sniptovertex(self):
        for i in range(len(self.x)):
            self.path.append([])
            for j in range(len(self.x[i])):
                min_dist = 1
                idn = 0
                for n in self.G.nodes_iter():
                    tmp = abs(self.x[i][j] - self.G.node[n]['x']) + abs(self.y[i][j] - self.G.node[n]['y'])
                    if tmp < min_dist:
                        min_dist = tmp
                        idn = n

   #             print(min_dist)
                self.path[i].append(idn)

  #      print(self.path)

    def drawTra(self, num):

        for i in range(len(self.path[num])-1):
             plt.plot([self.G.node[self.path[num][i]]['x'], self.G.node[self.path[num][i+1]]['x']], [self.G.node[self.path[num][i]]['y'], self.G.node[self.path[num][i+1]]['y']], 'b', linewidth=3)
#        for n in self.G.nodes_iter():
#            plt.plot(self.G.node[n]['x'], self.G.node[n]['y'], 'b.', linewidth=3)

        plt.plot(self.G.node[self.path[num][-1]]['x'], self.G.node[self.path[num][-1]]['y'], 'b.')

        for e in self.G.edges_iter():
            p1x = self.G.node[e[0]]['x']
            p1y = self.G.node[e[0]]['y']
            p2x = self.G.node[e[1]]['x']
            p2y = self.G.node[e[1]]['y']
            plt.plot([p1x, p2x], [p1y, p2y], c='r', linewidth=1)
        plt.show()



    def findshortest(self):
        for i in range(len(self.path)):
            self.trajectory.append([])
            shortest = nx.shortest_path(self.G, self.path[i][0], self.path[i][1])
            self.trajectory[i].extend(shortest)
            for j in range(1, len(self.path[i])-1):
                shortest = nx.shortest_path(self.G, self.path[i][j], self.path[i][j+1])
                self.trajectory[i].extend(shortest[1:])
           # print(self.trajectory[i])

        '''
        for i in range(len(self.trajectory[0])-1):
            plt.plot([self.G.node[self.trajectory[0][i]]['x'], self.G.node[self.trajectory[0][i+1]]['x']],
            [self.G.node[self.trajectory[0][i]]['y'], self.G.node[self.trajectory[0][i+1]]['y']], c='g', linewidth=5 )

        self.draw()
        '''
    def compute(self):
        if not self.integral:
            for i in range(len(self.trajectory)):
                self.integral.append([])

        for i in range(len(self.trajectory)):
            value = 0
            for j in range(len(self.trajectory[i])-1):
                v1 = self.trajectory[i][j]
                v2 = self.trajectory[i][j+1]
                weight = self.G.edge[v1][v2]['w']
                if v1 > v2:
                    weight = -weight
                value = value + weight
            self.integral[i].append(value)
  #          print(value)

    def drawall(self):
        for e in self.G.edges_iter():
            self.G.edge[e[0]][e[1]]['w'] = 0

        for i in range(len(self.trajectory)):
            for j in range(len(self.trajectory[i])):
                e0 = self.trajectory[i][j]
                e1 = self.trajectory[i][j+1]
                self.G.edge[e0][e1]['w'] += 1

        '''
        for e in self.G.edges_iter():
            p1x = self.G.node[e[0]]['x']
            p1y = self.G.node[e[0]]['y']
            p2x = self.G.node[e[1]]['x']
            p2y = self.G.node[e[1]]['y']
            plt.plot([p1x, p2x], [p1y, p2y], c='gray')
        '''


        for e in self.G.edges_iter():
            if self.G.edge[e[0]][e[1]]['w'] > 0:
                p1x = self.G.node[e[0]]['x']
                p1y = self.G.node[e[0]]['y']
                p2x = self.G.node[e[1]]['x']
                p2y = self.G.node[e[1]]['y']
                plt.plot([p1x, p2x], [p1y, p2y], c='b', linewidth=self.G.edge[e[0]][e[1]]['w']/10+1)

        self.drawhole()

        plt.plot([self.G.node[self.trajectory[i][0]]['x']],
                 [self.G.node[self.trajectory[i][0]]['y']], 'ro', markersize=15)
        plt.plot([self.G.node[self.trajectory[i][-1]]['x']],
                 [self.G.node[self.trajectory[i][-1]]['y']], 'r^', markersize=15)

        plt.xlim(-0.02, 1)
        plt.ylim(0, 1)
       # plt.show()


    def drawhole(self, out=0, col='black'):
        if out:
            lenIn0 = len(self.innerpath[0])
            for i in range(lenIn0):
                p1 = self.innerpath[0][i]
                if i+1 >= lenIn0:
                    p2 = self.innerpath[0][0]
                else:
                    p2 = self.innerpath[0][i+1]

                p1x = self.inner.node[p1]['x']
                p1y = self.inner.node[p1]['y']
                p2x = self.inner.node[p2]['x']
                p2y = self.inner.node[p2]['y']
                plt.plot([p1x, p2x], [p1y, p2y], color=col, linewidth=3)

        lenIn = len(self.innerpath)
        print self.innerpath
        for i in range(1, lenIn):
            px = []
            py = []
            lenI = len(self.innerpath[i])
            for j in range(lenI):
                px.append(self.inner.node[self.innerpath[i][j]]['x'])
                py.append(self.inner.node[self.innerpath[i][j]]['y'])
            plt.fill(px, py, color=col)

    def drawTra2(self, traid, dr=0, drout=0, colHole='black'):
        if len(traid) == 3:
            c =['#003300', '#009900', '#00FF00']
        elif len(traid) == 2:
            c = ['#00CC00', '#0033FF']
        elif len(traid) == 4:
            c = ['#00CC00', '#0033FF', '#CC0000', '#A6ABAB']
        else:
            #c = ['#006600', '#00FF00', '#0033FF', '#00CCFF']
            #c = ['#00CC00', '#0033FF', '#CC0000', '#996600']
            c = ['#11ED23', '#0A8A14', '#044709', '#6677E3', '#283BB0', '#0A1878', '#ED694C', '#D10A0A', '#B00707']


        if len(traid) == 2:
            lw = [6, 4]
        elif len(traid) == 9:
            lw = [1.5 for i in range(2, 11)]
        else:
            lw = [3, 3, 3, 3]

        print(lw)
        print(c)

        counter = 0
        if dr == 1:
            for e in self.G.edges_iter():
                p1x = self.G.node[e[0]]['x']
                p1y = self.G.node[e[0]]['y']
                p2x = self.G.node[e[1]]['x']
                p2y = self.G.node[e[1]]['y']
                plt.plot([p1x, p2x], [p1y, p2y], color='gray', linewidth=1)

        self.drawhole(drout, col=colHole)

        for i in traid:
#            print(self.trajectory[i])
            print(counter)
            for j in range(len(self.trajectory[i])-1):
 #               print('%d,%d' % (self.trajectory[i][j], self.trajectory[i][j+1]))
                plt.plot([self.G.node[self.trajectory[i][j]]['x'], self.G.node[self.trajectory[i][j+1]]['x']],
                         [self.G.node[self.trajectory[i][j]]['y'], self.G.node[self.trajectory[i][j+1]]['y']], color=c[counter], linewidth=lw[counter], alpha=0.7)
            counter += 1

        i = traid[0]
      #  print(traid)
       # print([self.G.node[self.trajectory[i][0]]['x'], self.G.node[self.trajectory[i][-1]]['x']])
        plt.plot([self.G.node[self.trajectory[i][0]]['x']],
                 [self.G.node[self.trajectory[i][0]]['y']], 'ro', markersize=15)
        plt.plot([self.G.node[self.trajectory[i][-1]]['x']],
                 [self.G.node[self.trajectory[i][-1]]['y']], 'r^', markersize=15)

        plt.xlim(-0.02, 1)
        plt.ylim(0, 1)





      #  plt.show()


    def drawTraList(self, traid, dr=0, drout=0, colHole='black'):
        if len(traid) == 3:
            c =['#003300', '#009900', '#00FF00']
        elif len(traid) == 2:
            c = ['#00CC00', '#0033FF']
        elif len(traid) == 4:
            c = ['#00CC00', '#0033FF', '#CC0000', '#A6ABAB']
        else:
            #c = ['#006600', '#00FF00', '#0033FF', '#00CCFF']
            #c = ['#00CC00', '#0033FF', '#CC0000', '#996600']
            c = ['#11ED23', '#0A8A14', '#044709', '#6677E3', '#283BB0', '#0A1878', '#ED694C', '#D10A0A', '#B00707']


        if len(traid) == 2:
            lw = [6, 4]
        elif len(traid) == 9:
            lw = [1.5 for i in range(2, 11)]
        else:
            lw = [3, 3, 3, 3]

        print(lw)
        print(c)

        counter = 0
        if dr == 1:
            for e in self.G.edges_iter():
                p1x = self.G.node[e[0]]['x']
                p1y = self.G.node[e[0]]['y']
                p2x = self.G.node[e[1]]['x']
                p2y = self.G.node[e[1]]['y']
                plt.plot([p1x, p2x], [p1y, p2y], color='gray', linewidth=1)

        self.drawhole(drout, col=colHole)

        for i in len(traid):
#            print(self.trajectory[i])
            print(counter)
            for j in traid[i]:
 #               print('%d,%d' % (self.trajectory[i][j], self.trajectory[i][j+1]))
                plt.plot([self.G.node[j]['x'], self.G.node[j]['x']],
                         [self.G.node[j]['y'], self.G.node[j]['y']], color=c[counter], linewidth=lw[counter], alpha=0.7)
            counter += 1

    def drawTraNew(self, traid, newTra, dr=1, drout=0, colHole='black'):
        if len(traid) == 3:
            c =['#003300', '#009900', '#00FF00']
        elif len(traid) == 2:
            c = ['#00CC00', '#0033FF']
        elif len(traid) == 4:
            c = ['#00CC00', '#0033FF', '#CC0000', '#A6ABAB']
        elif len(traid) == 1:
            c = ['#00CC00', '#0033FF']
        else:
            #c = ['#006600', '#00FF00', '#0033FF', '#00CCFF']
            #c = ['#00CC00', '#0033FF', '#CC0000', '#996600']
            c = ['#11ED23', '#0A8A14', '#044709', '#6677E3', '#283BB0', '#0A1878', '#ED694C', '#D10A0A', '#B00707']


        if len(traid) == 2:
            lw = [6, 4]
        elif len(traid) == 9:
            lw = [1.5 for i in range(2, 11)]
        else:
            lw = [3, 3, 3, 3]

        print(lw)
        print(c)

        counter = 0
        if dr == 1:
            for e in self.G.edges_iter():
                p1x = self.G.node[e[0]]['x']
                p1y = self.G.node[e[0]]['y']
                p2x = self.G.node[e[1]]['x']
                p2y = self.G.node[e[1]]['y']
                plt.plot([p1x, p2x], [p1y, p2y], color='gray', linewidth=1)

        self.drawhole(drout, col=colHole)

        for i in traid:
#            print(self.trajectory[i])
            print(counter)
            for j in range(len(self.trajectory[i])-1):
 #               print('%d,%d' % (self.trajectory[i][j], self.trajectory[i][j+1]))
                plt.plot([self.G.node[self.trajectory[i][j]]['x'], self.G.node[self.trajectory[i][j+1]]['x']],
                         [self.G.node[self.trajectory[i][j]]['y'], self.G.node[self.trajectory[i][j+1]]['y']], color=c[counter], linewidth=lw[counter], alpha=0.7)
            counter += 1

        for i in traid:
            print(newTra[i])
            print(counter)
            for j in range(len(newTra[i])-1):
 #               print('%d,%d' % (newTra[i][j], newTra[i][j+1]))
                plt.plot([self.G.node[newTra[i][j]]['x'], self.G.node[newTra[i][j+1]]['x']],
                         [self.G.node[newTra[i][j]]['y'], self.G.node[newTra[i][j+1]]['y']], color=c[counter], linewidth=lw[counter], alpha=0.7)
            counter += 1

        i = traid[0]
      #  print(traid)
       # print([self.G.node[newTra[i][0]]['x'], self.G.node[newTra[i][-1]]['x']])
        plt.plot([self.G.node[newTra[i][0]]['x']],
                 [self.G.node[newTra[i][0]]['y']], 'ro', markersize=15)
        plt.plot([self.G.node[newTra[i][-1]]['x']],
                 [self.G.node[newTra[i][-1]]['y']], 'r^', markersize=15)


        pylab.show()
        plt.xlim(-0.02, 1)
        plt.ylim(0, 1)

#moma
def moma(trlist, polyname = 'moma_floor_plan.poly', comp=0, drout=1):
    m = homotopypath()
    #m.readfile('./basis2/Shenzhen_0.dv.m')
    m.readfile('./moma_2_basis/moma_2_0.dv.m')

    #m.draw()
    f = open('momapath1.txt', 'r')
    m.path = pickle.load(f)
    f.close()

    #m.drawhole()

    m.findshortest()
    m.readpoly(polyname)

    if comp:
        filelist = ['./moma_2_basis/moma_2_' + str(i) + '.dv.m' for i in range(6)]
        for name in filelist:
            print(name)
            m.readdv(name)
            m.compute()
        print(m.integral)


    m.drawTra2(trlist, drout=1)
    plt.axis('off')
    plt.savefig("test.pdf", bbox_inches='tight', transparent=True)


#shenzhen 3 ho


def shenzhen7(tralist=[], traname='tr2.txt', polyname='shenzhen7.poly', comp=0):
    dim = 7
    m = homotopypath()
    m.readfile('./basis7/Shenzhen_0.dv.m')
    m.readtra(traname)
    #m.readtra('tr.txt')
    m.sniptovertex()

    m.readpoly(polyname)

    #m.drawTra(79)
    m.findshortest()
  #  m.drawall()
    #m.drawTra(0)
    #m.drawTra(1)
#    print (m.trajectory)
#    print(len(m.trajectory))
    if comp:
        filelist = ['./basis7/Shenzhen_' + str(i) + '.dv.m' for i in range(dim)]
        for name in filelist:
            print(name)
            m.readdv(name)
            m.compute()
        print(m.integral)

    filename = open('shenzhensave.txt', 'w')
    pickle.dump(m, filename)
    filename.close()

    #m.drawTra2([52, 71])

    # m.drawTra2([0, 2])

    #m.drawTra2([1, 14])
    '''
    m.drawTra2(tralist, colHole='gray')
    plt.axis('off')
    plt.savefig("shenzhen7.pdf", bbox_inches='tight', transparent=True)
'''

    #m.drawTra2([20, 82])

def shenzhen5(traname='tr2.txt', polyname='shenzhen7.poly', comp=0):
    dim = 5
    m = homotopypath()
    m.readfile('./basis5/shenzhen5_1_0.dv.m')
    m.readtra(traname)

    m.sniptovertex()

    m.readpoly(polyname)

    #m.drawTra(79)
    m.findshortest()
    if comp:
        filelist = ['./basis5/shenzhen5_1_' + str(i) + '.dv.m' for i in range(dim)]
        for name in filelist:
            print(name)
            m.readdv(name)
            m.compute()
        print(m.integral)


def shenzhen3(traname='tr2.txt', polyname='shenzhen7.poly', comp=0):
    dim = 3
    m = homotopypath()
    m.readfile('./basis3/shenzhen3_1_0.dv.m')
    m.readtra(traname)

    m.sniptovertex()

    m.readpoly(polyname)

    #m.drawTra(79)
    m.findshortest()
    if comp:
        filelist = ['./basis3/shenzhen3_1_' + str(i) + '.dv.m' for i in range(dim)]
        for name in filelist:
            print(name)
            m.readdv(name)
            m.compute()
        print(m.integral)




def shenzhen7Draw(traname='tr2.txt', polyname='shenzhen7.poly'):
    dim = 7
    m = homotopypath()
    m.readfile('./basis7/Shenzhen_0.dv.m')
    m.readpoly(polyname)
    m.readtra(traname)
    #m.readtra('tr.txt')
    m.sniptovertex()

    #m.drawTra(79)
    m.findshortest()
    m.drawall()
    plt.axis('off')
    plt.savefig("trajectory.eps", bbox_inches='tight')

def tra7():
    dim = 7
    m = homotopypath()
    m.readfile('./basis7/Shenzhen_0.dv.m')
    m.readtra('trajectory.txt')
    #m.readtra('tr.txt')
    m.sniptovertex()

    #m.drawTra(79)
    m.findshortest()

    m.trajectory
    filename = open('trashenzhen7.txt', 'w')
    pickle.dump(m.trajectory, filename)
    filename.close()
#shenzhen5(52, 31)
#shenzhen7([84, 6, 179, 81], 'tr2.txt')
#shenzhen7Draw()
#moma([0, 19, 26, 1, 11, 21, 2, 46, 62], drout=1)

def moma2(trlist=[], polyname = 'moma_floor_plan.poly', comp=0, drout=1):
    m = homotopypath()
    #m.readfile('./basis2/Shenzhen_0.dv.m')
    m.readfile('./moma_2_basis/moma_2_0.dv.m')


    m.readpoly(polyname)
    m.drawhole(out=1)

    plt.axis('off')
    plt.savefig("hole.pdf", bbox_inches='tight', transparent=True)


#shenzhen7()
#shenzhen5(comp=1)

shenzhen7(traname = 'trtest.txt')


filename = open('shenzhensave.txt')
m = pickle.load(filename)
filename.close()

meet = dict()
for i in range(len(m.trajectory)):
    for j in range(len(m.trajectory[i])):
        key = m.trajectory[i][j]
        if meet.has_key(key):
            meet[key].append(i)
        else:
            meet[key] = [i]

exchange = dict()

for key in meet:
    if key == 192 or key == 386:  #start
        continue

    l1 = list(set(meet[key]))
    if len(l1) > 1:
        l2 = l1[:]
        random.shuffle(l2)
        for i in range(len(l1)):
            exchange[(l1[i], key)] = l2[i]
#print(exchange)




newTra = []
#for i in range(len(m.trajectory)):
for i in range(len(m.trajectory)):
    newTra.append([192])
    tmp = m.trajectory[i][1]
    myid = i
    pos = 1
    while tmp != 386:
        newTra[i].append(tmp)
        if (myid, tmp) in exchange:
            pre = myid
            myid = exchange[(myid, tmp)]
            del exchange[(pre, tmp)]

            pos = m.trajectory[myid].index(tmp) + 1


  #          print('(%d,%d)' % (myid, m.trajectory[myid][pos]))
        else:
            pos += 1

        tmp = m.trajectory[myid][pos]
    newTra[i].append(386)
print('tra')
print(m.trajectory)
print('newTra      ')
print(newTra)
m.drawTraNew([0], newTra=newTra)

filename = open('exchange.txt', 'w')
pickle.dump(exchange, filename)
filename.close()
filename = open('newTra.txt', 'w')
pickle.dump(newTra, filename)
filename.close()

plt.axis('off')
plt.savefig("1.pdf", bbox_inches='tight', transparent=True)


dim = 7
filelist = ['./basis7/Shenzhen_' + str(i) + '.dv.m' for i in range(dim)]
for name in filelist:
    print(name)
    m.readdv(name)
    m.compute()
print()
print(m.integral)
m.trajectory = newTra
for name in filelist:
    print(name)
    m.readdv(name)
    m.compute()
print()
print(m.integral)

#print(exchange)













