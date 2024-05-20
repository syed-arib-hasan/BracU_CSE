import graph_creator
f1=open("input.txt","r")
l=[]
n,m=map(int,f1.readline().strip().split(" "))
for i in range (m):
    l.append(map(int,f1.readline().strip().split(" ")))
graph=graph_creator.undirected_unwei_graph(l,n,m)
print(graph)

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
