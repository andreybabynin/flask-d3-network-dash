import networkx as nx
from networkx.readwrite.json_graph import node_link_data
import pandas as pd
from itertools import combinations

class Network():
    def __init__(self):
        pass
    
    def json_graph(self, df):
        network_df, dic_attr = self._find_connections(df)
        
        G = nx.from_pandas_edgelist(network_df, 
                    'Ticker', 'Target', edge_attr='Weight', create_using=nx.Graph)
        
        nx.set_node_attributes(G, dic_attr , "occurence")
        
        return node_link_data(G)
     
        
    def find_all_stocks(self, l, dic_attr):
        for i in l:
            if i not in dic_attr.keys():
                dic_attr[i] = 1
            else:
                dic_attr[i] += 1
        return dic_attr
    
    def _find_connections(self, df):
        
        dic_m = {} # for storing edges
        dic_attr = {} #for storing nodes attribtues
        for row in df['mentioned'].tolist():
            list1 = row.split(' ')
            list1.remove(df.at[0, 'ticker'])
            
            if len(list1) >1:
                dic_attr = self.find_all_stocks(list1, dic_attr)
            
            if list1 != None:
                comb = list(combinations(list1, 2))
                for i in comb:
                    if (i in dic_m.keys()) or ((i[1], i[0]) in dic_m.keys()):
                        try:
                            dic_m[i] += 1
                        except: dic_m[(i[1], i[0])] += 1
                    else:
                        dic_m[i] = 1
        list1 = []
        for k,v in dic_m.items():
            list1.append([k[0], k[1], v])
        return pd.DataFrame(list1, columns = ['Ticker', 'Target', 'Weight']), dic_attr
    
#n = Network()  

#n._find_connections(df)





