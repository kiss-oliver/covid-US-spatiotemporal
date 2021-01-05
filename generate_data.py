import networkx as nx
import pandas as pd
import json

raw_neighborhoods = pd.read_csv('data/county_adjacency.txt', sep='\t', dtype=object, encoding='ISO-8859-1', header=None, names=['x','FIPS_x','y','FIPS_y'])
filled_neighborhoods = raw_neighborhoods.fillna(method='ffill')
filled_neighborhoods = filled_neighborhoods[filled_neighborhoods.FIPS_x!='51515']
filled_neighborhoods = filled_neighborhoods[filled_neighborhoods.FIPS_y!='51515']

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

data = {}
fips_to_node_id = {x[1]['fips']:x[0] for x in list(relabeled.nodes(data=True))}
data['node_ids'] = fips_to_node_id
data['edges'] = [line.split() for line in nx.generate_edgelist(relabeled, data=False)]

cases = pd.read_csv('data/covid_confirmed_usafacts.csv', dtype=object)
cases.loc[cases.countyFIPS=='46102','countyFIPS'] = '46113'
cases['nodeid'] = cases['countyFIPS'].map(lambda x: fips_to_node_id[(5-len(str(x)))*'0'+str(x)] if (5-len(str(x)))*'0'+str(x) in fips_to_node_id.keys() else '')
cases = cases[cases.nodeid!='']
cases = cases[[x for x in list(cases) if x not in ['1/22/20', '1/23/20', '1/24/20', '1/25/20', '1/26/20', '1/27/20', '1/28/20', '1/29/20', '1/30/20', '1/31/20', '2/1/20', '2/2/20', '2/3/20', '2/4/20', '2/5/20', '2/6/20', '2/7/20', '2/8/20', '2/9/20', '2/10/20', '2/11/20', '2/12/20', '2/13/20', '2/14/20', '2/15/20']]]


sorted = cases.sort_values('nodeid')
dates = [x for x in list(sorted) if '/' in x]
data['time_periods'] = len(dates)

for index in range(len(dates)):
    i = str(index)
    data[i] = {}
    data[i]['index'] = index
    data[i]['y'] = sorted[dates[index]].tolist()
    data[i]['month'] = int(dates[index].split('/')[0])
    data[i]['day'] = int(dates[index].split('/')[1])
    data[i]['year'] = int('20'+dates[index].split('/')[2])

mobility = pd.read_csv('data/2020_US_Region_Mobility_Report.csv', dtype=object)
mobility.loc[mobility.census_fips_code=='46102','census_fips_code'] = '46113'
mobility['nodeid'] = mobility['census_fips_code'].map(lambda x: fips_to_node_id[(5-len(str(x)))*'0'+str(x)] if (5-len(str(x)))*'0'+str(x) in fips_to_node_id.keys() else '')
mobility = mobility[mobility.nodeid!='']

for index in range(len(dates)):
    i = str(index)
    date = '{}-{}-{}'.format(data[i]['year'],'0'*(2-len(str(data[i]['month'])))+str(data[i]['month']),'0'*(2-len(str(data[i]['day'])))+str(data[i]['day']))
    mobility_section = mobility[mobility.date==date]
    mobility_section_sorted = mobility_section.append(pd.DataFrame({'nodeid':[x for x in range(len(fips_to_node_id)) if x not in mobility_section.nodeid.tolist()]})).sort_values('nodeid')
    data[i]['X'] = mobility_section_sorted[['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline']].values.tolist()

json.dump(data,open('covid-spatiotemporal.json','w'))
