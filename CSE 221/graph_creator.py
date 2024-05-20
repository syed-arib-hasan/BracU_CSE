def directed_graph(list,vertices,edges):
    graph={}
    for i in range(1,vertices+1):
        graph[i]=[]
    for i in range (edges):
        u,v,w=list[i]
        graph[u].append((v,w))
    return graph

def directed_unwei_graph(list,vertices,edges):
    graph={}
    for i in range(1,vertices+1):
        graph[i]=[]
    for i in range (edges):
        u,v=list[i]
        graph[u].append(v)
    return graph



def undirected_graph(list,vertices,edges):
    graph={}
    for i in range(1,vertices+1):
        graph[i]=[]
    for i in range (edges):
        u,v,w=list[i]
        graph[u].append((v,w))
        graph[v].append((u,w))
    return graph

def undirected_unwei_graph(list,vertices,edges):
    graph={}
    for i in range(1,vertices+1):
        graph[i]=[]
    for i in range (edges):
        u,v=list[i]
        graph[u].append(v)
        graph[v].append(u)
    return graph
    
# f1=open("input.txt","r")
# v,e=map(int,f1.readline().strip().split(" "))
# l=[]
# for i in range (v):
#     l.append(map(int,f1.readline().strip().split(" ")))
# print(undirected_graph(l,v,e))



    