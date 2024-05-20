import graph_creator
f1=open("input.txt","r")
l=[]
n,m=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.directed_unwei_graph(l,n,m)

def is_cycle(graph):
    visited = ["Not Visited"]*(len(graph)+1)
    cycle = False 
    def DFS(source = 1):
        nonlocal visited, cycle
        visited[source] = "Discovered"
        for neighbour in graph[source]:
            if(visited[neighbour] == "Discovered"):
                cycle = True 
            elif(visited[neighbour] == "Not Visited"):
                DFS(neighbour)
        visited[source] = "Explored"
    for i in graph:
        if(visited[i] == "Not Visited"):
            DFS(i)
    return cycle 

print(graph)
print(is_cycle(graph))

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