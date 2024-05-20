import graph_creator
import find_cycle
f1=open("input.txt","r")
l=[]
n,m=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.directed_unwei_graph(l,n,m)

def topo_sort(graph,n,m):
    if find_cycle.is_cycle(graph)== True:
        return "mama pssible na.......possible hoile kortam"
    in_degree=[float("inf")]*(n+1)
    for i in graph:
        temp=i
        c=0
        for value in graph.values():
            if temp in value:
                c+=1
        in_degree[temp]=c

    q=[i for i in range(1,len(in_degree)) if in_degree[i]==0]
    visited=[]
    while q:
        current_node=q.pop(0)
        for neighbor in graph[current_node]:
            in_degree[neighbor]=in_degree[neighbor]-1
            if in_degree[neighbor]==0:
                q.append(neighbor)
                #q.sort()
        visited.append(current_node)
    return visited

print(graph)
print(topo_sort(graph,n,m))