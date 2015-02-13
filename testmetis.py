__author__ = 'aladdin'
import networkx as nx
import metis
G = metis.example_networkx()

for n in G.nodes_iter():
    print n
metis.part_graph(G,2)
'''
(edgecuts, parts) = metis.part_graph(G, 3)
colors = ['red','blue','green']
for i, p in enumerate(parts):
    G.node[i]['color'] = colors[p]
nx.write_dot(G, 'example.dot') # Requires pydot or pygraphviz
'''