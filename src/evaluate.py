import networkx as nx

from src.load_data import load_BREC_data, load_other_data
from src.check_iso import check_if_graphs_are_isomorphic

def evaluate_on_BREC(max_dim: int = 4, Rips: bool = False) -> dict:

    all_graphs = load_BREC_data()
    results ={}

    for dim in range(1, max_dim+1):
        print(dim)
        results[f"dimension {dim}"] = {}
        for graph_battery, graphs in all_graphs.items():
            print(graph_battery)
            score = 0
            total = 0
            if graph_battery in {
                'basic',
                'strongly regular',
                '4vtx'
            }:
                
                total = len(graphs)/2
                for i in range(0, len(graphs), 2):
                    
                    G1 = nx.from_graph6_bytes(graphs[i].encode())
                    G2 = nx.from_graph6_bytes(graphs[i+1].encode())
                    score += 1 - check_if_graphs_are_isomorphic(G1, G2, max_dim=dim, Rips=Rips)
            
            if graph_battery == 'DR':
                total = len(graphs)/2
                for i in range(0, len(graphs), 2):
                    
                    G1 = nx.from_graph6_bytes(graphs[i])
                    G2 = nx.from_graph6_bytes(graphs[i+1])
                    score += 1 - check_if_graphs_are_isomorphic(G1, G2, max_dim=dim, Rips=Rips)


            if graph_battery in {
                'regular',
                'CFI'
            }:
                total = len(graphs)
                for pair in graphs:
            
                    G1 = nx.from_graph6_bytes(pair[0])
                    G2 = nx.from_graph6_bytes(pair[1])
                    score += 1 - check_if_graphs_are_isomorphic(G1,G2, max_dim=dim, Rips=Rips)

            if graph_battery =='extension':
                total = len(graphs)
                for pair in graphs:
            
                    G1 = nx.from_graph6_bytes(pair[0].encode())
                    G2 = nx.from_graph6_bytes(pair[1].encode())
                    score += 1 - check_if_graphs_are_isomorphic(G1,G2, max_dim=dim, Rips=Rips)

            results[f"dimension {dim}"][graph_battery] = score/total 
            
    return results 

def evaluate_on_other(max_dim: int = 4, Rips: bool = False) -> dict:
    all_graps = load_other_data()
    results ={}

    for dim in range(max_dim+1):
        results[f"dimension {dim}"] = {}
        for graph_battery, graphs in all_graps.items():
            score = 0
            total = len(graphs)/2

            for i in range(0, len(graphs), 2):

                G1 = graphs[i]
                G2 = graphs[i+1]
                score += 1 - check_if_graphs_are_isomorphic(G1, G2, max_dim=max_dim, Rips=Rips)

            results[f"dimension {dim}"][graph_battery] = score/total

    return results

