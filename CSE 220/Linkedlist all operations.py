import numpy as np
class Node:
    def __init__ (self,elem,next=None):
        self.elem=elem
        self.next=next

def createlist(arr):
    head=Node(arr[0])
    tail=head
    for i in range (1,len(arr)):
        n=Node(arr[i])
        tail.next=n
        tail=n
    return head

def printll(head):
    temp=head
    while temp:
        if temp.next==None:
            print(temp.elem)
        else:
            print(temp.elem,"--> ",end="")
        temp=temp.next

def count(head):
    c=0
    temp=head
    while temp!=None:
        c+=1
        temp=temp.next
    return c

def elemat(head,idx):
    temp=head
    count=0
    while temp:
        if count== idx:
            return temp.elem
        temp=temp.next
        count+=1
    return "invalid index"

def nodeat(head,idx):
    count=0
    temp=head
    while temp:
        if count==idx:
            return temp
        temp=temp.next
        count+=1
    return "Invalid index"           

def setelem(head,idx,elem):
    temp=nodeat(head,idx)
    temp.elem=elem
    
def insertelem(head,elem,idx):
    total_nodes=count(head)
    if idx==0:
      n=Node(elem,head)
      head=n
    elif idx==total_nodes:
      n=Node(elem)
      n1=nodeat(head,idx-1)
      n1.next=n
    elif 0<idx<total_nodes:
      n1=nodeat(head,idx-1)
      n2=nodeat(head,idx)
      n=Node(elem)
      n1.next=n
      n.next=n2
    else:
      print("Invalid")
    return head

def remove(head,idx):
    if idx==count(head):
        n1=nodeat(head,idx-1)
        n1.next=None
    elif idx==0:
        head=head.next
       
    elif 0<idx<count(head):
        n1=nodeat(head,idx-1)
        n2=nodeat(head,idx+1)
        n1.next=n2
    return head

def copylist(source):
    temp=source
    copy_head=None
    copy_tail=None
    while temp:
        n=Node(temp.elem)
        if copy_head==None:
            copy_head=n
            copy_tail=copy_head
        else:
            copy_tail.next=n
            copy_tail=n
        temp=temp.next
    return copy_head

def reverse(head):
    new_head=Node(head.elem)
    temp=head.next
    while temp:
        n=Node(temp.elem,new_head)
        new_head=n
        temp=temp.next
    return new_head

def rotateleft(head):
  temp=head
  new_head=head.next
  while temp:
    if temp.next==None:
      temp.next=head
      head.next=None
    temp=temp.next
  head=new_head
  return(head)
    
def rotateright(head,n):
    last=head
    seclast=None
    k=nodeat(head,count(head)-1-n)
    while last!=None:
        if last.next==None:
            last.next=head
            head=k.next
            k.next=None
            return (head)
        seclast=last
        last=last.next


head = createlist(np.array([13,10,6,20,17]))
printll(head)
print("Retrieving an element:",elemat(head,4))
print("Retrieving an node:",nodeat(head,4))
setelem(head,3,25)
print("updated value: ",end="")
printll(head)
print(count(head))
print("Inserted new node:",end=" ")
x=insertelem(head,50, 5)
printll(x)
print("Removed node: ",end="")
printll(remove(head,4))
print("Copied List:",end=" ")
printll(copylist(head))
# print("Left Rotated list: ",end="")     ### you can run rotate right funtion or rotate left function at a time. Comment out one and run another one or else u will get error
# printll(rotateleft(head))
print("Right Rotated list: ",end="")
printll(rotateright(head,2))
