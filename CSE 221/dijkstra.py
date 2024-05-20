import graph_creator
f1=open("input.txt","r")
l=[]
n,m=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.directed_graph(l,n,m)
s=int(f1.readline())

import heapq

def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * (n+1)
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist[1:]


print(dijkstra(graph,s))