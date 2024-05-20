import graph_creator
f1=open("input.txt","r")
l=[]
n,m=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.directed_graph(l,n,m)
s=int(f1.readline())

def bfs(graph,start_node=1):
    visited=[0]*(len(graph)+1)
    result=[]
    q=[start_node]
    while q:
        cn=q.pop(0)
        if visited[cn]==0:
            result.append(cn)
            visited[cn]=1
        for n in graph[cn]:
            if visited[n]==0:
                q.append(n)

    for i in range(1,len(visited)):
        if visited[i]==0:
            bfs(i+1)
    return result

print(bfs(graph))


def dfs(graph, start_node=1, visited=None):
    if visited is None:
        visited = [0] * (len(graph) + 1)
    result = []
    result.append(start_node)
    visited[start_node] = 1    
    for neighbor in graph[start_node]:
        if visited[neighbor] == 0:
            result.extend(dfs(graph, neighbor, visited))    
    for i in range(1, len(visited)):
        if visited[i] == 0:
            result.extend(dfs(graph, i, visited))
    
    return result


print(dfs(graph))


def cycle(graph):
    visited=[0]*(len(graph)+1)
    c=False
    def dfs(source=1):
        nonlocal visited,c
        visited[source]=1
        for n in graph[source]:
            if visited[n]==1:
                c=True
            elif visited[n]==0:
                dfs(n)
        visited[source]=-1

    for i in graph:
        if visited[i]==0:
            dfs(i)
    return c

print(cycle(graph))
import heapq
def dijkastra(graph,source):
    n=len(graph)
    dist=[float('inf')]*(n+1)
    dist[source]=0
    pq=[(0,source)]
    while pq:
        d,u=heapq.heapop(pq)
        if d>dist[u]:
            continue
        for v,w in graph[u]:
            if dist[u]+w<dist[v]:
                dist[v]=dist[u]+w
                heapq.heappush(pq,(dist[v],v))

    return dist[1:]

def dj(graph,source):
    dist=[float("inf")]*(len(graph)+1)
    dist[source]=0
    pq=[(0,source)]
    while pq:
        d,u=heapq.pop(pq)
        if d>dist[u]:
            continue
        for v,w in graph[u]:
            if dist[u]+w<dist[v]:
                dist[v]=dist[u]+w
                heapq.headpush(pq,(dist[v],v))

    return dist[1:]

