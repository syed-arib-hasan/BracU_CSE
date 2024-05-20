import graph_creator
f1=open("input.txt","r")
l=[]
n,m,t=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.undirected_unwei_graph(l,n,m)

def shortest_path(graph, start_node, target):
    visited = []
    q = [[start_node]]
    while q:
        path = q.pop(0)
        current_node = path[-1]
        if current_node == target:
            return path
        if current_node not in visited:
            visited.append(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                new_path = list(path) 
                new_path.append(neighbor)
                q.append(new_path)
    return []  
print(shortest_path(graph,1,t))