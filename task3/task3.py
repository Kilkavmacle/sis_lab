import pandas
import numpy
import csv
import math

def main(graph):

    S = numpy.zeros((graph['end'].max(), 5), int)

    for node in range(1, graph['end'].max() + 1):
        Outdegree = graph[graph['begin'] == node]['end'].count()
        Indegree = graph[graph['end'] == node]['begin'].count()
        Secondary_neighbors_out = graph[graph['begin'].isin(graph[graph['begin'] == node]['end'])]['end'].count()
        Secondary_neighbors_in = graph[graph['end'].isin(graph[graph['end'] == node]['begin'])]['begin'].count()
        Relation = graph[graph['begin'].isin(graph[graph['end'] == node]['begin'])]['end'].count()
        
        if Relation != 0:
            Relation -= 1

        S[node - 1] = [Outdegree, Indegree, Secondary_neighbors_out, Secondary_neighbors_in, Relation]

    return S

    graph.columns = ['begin', 'end']
    result = main(graph)
    for i in range(len(result)):
        print(f"Node {i+1}", result[i])

def task(graph):
    S1 = main(graph)
    e = 0

    for i in range(graph['end'].max()):
        for j in range(5):
            if S1[i][j] != 0:
                e += (S1[i][j] / (graph['end'].max() - 1)) * math.log(S1[i][j] / (graph['end'].max() - 1), 2)
                
    return -e

if __name__ == "__main__":
    graph = pandas.read_csv('./task3/graph.csv', sep=',')
    graph.columns = ['begin', 'end']
    result = task(graph)
    print("Entropy =", result)
