import graph_creator
f1=open("input.txt","r")
l=[]
n,m=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.undirected_unwei_graph(l,n,m)
print(graph)

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