import networkx as nx
import pandas as pd

raw_neighborhoods = pd.read_csv('data/county_adjacency.txt', sep='\t', dtype=object, encoding='ISO-8859-1', header=None, names=['x','FIPS_x','y','FIPS_y'])
filled_neighborhoods = raw_neighborhoods.fillna(method='ffill')

all_fips = list(set(filled_neighborhoods.FIPS_x.tolist()+filled_neighborhoods.FIPS_y.tolist()))
fips_to_node_id = dict(zip(all_fips,range(len(all_fips))))
node_id_to_fips = dict(zip(range(len(all_fips)),all_fips))

edges = zip(filled_neighborhoods.FIPS_x.map(lambda x: fips_to_node_id[x]).tolist(),filled_neighborhoods.FIPS_y.map(lambda x: fips_to_node_id[x]).tolist())

G = nx.Graph()
for i in range(len(all_fips)):
    G.add_node(i, fips=node_id_to_fips[i])

for edge in edges:
    G.add_edge(edge[0],edge[1])

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
largest_cc = G.subgraph(Gcc[0])
relabeled = nx.convert_node_labels_to_integers(largest_cc)

nx.write_gpickle(relabeled, "data/county_adjacency.gpickle")
