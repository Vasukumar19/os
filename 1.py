"""class IndexedAllocation:
    def __init__(self,size):
        self.disk=[0]*size
    def allocate(self,indexed_block,blocks):
        if self.disk[indexed_block]==0 and all(self.disk[b]==0 for b in blocks):
            self.disk[indexed_block]=blocks
            for b in blocks:
                self.disk[b]=1
            print("Allocation successful")
        else:
            print("Allocation failed")
f=IndexedAllocation(20)
f.allocate(5,[2,3,4])

class LinkedAllocation:
    def __init__(self,size):
        self.disk=[None]*size
    def allocate(self,blocks):
        for i in range(len(blocks)-1):
            self.disk[blocks[i]]=blocks[i+1]
        self.disk[blocks[-1]]=-1
        print("Allocation successful")
f=LinkedAllocation(20)
f.allocate([2,3,4,5])

class ContiguousAllocation:
    def __init__(self,size):
        self.disk=[0]*size
    def allocate(self,start,length):
        if all(self.disk[b]==0 for b in range(start,start+length)):
            for b in range(start,start+length):
                self.disk[b]=1
            print(f"file allocated from {start } to {start+length}")
        else:
            print("not enough contiguous space")
f=ContiguousAllocation(20)
f.allocate(2,5)

import threading
import time
import random
from queue import Queue

buffer=Queue(maxsize=5)

def producer():
    while True:
        item=random.randint(1,100)
        buffer.put(item)
        print(f'item produce{item}')
        time.sleep(random.random())
def consumer():
    while  True:
        item=buffer.get()
        print(f'item consume{item}')
        time.sleep(random.random())
threading.Thread(target=producer,daemon=True).start()
threading.Thread(target=consumer,daemon=True).start()

time.sleep(10)

import threading
import time
N=5
forks=[threading.Semaphore(1) for _ in range(N)]

def philosopher(i):

    left,right=forks[i],forks[(i+1)%N]

    while True:
        print(f'philosopher {i} is thinking')
        time.sleep(1)
        print(f'philosopher {i} is hungry')

        with left:
            with right:
                print(f'philosopher {i} is eating')
                time.sleep(1)
for i in range(N):
    threading.Thread(target=philosopher,args=(i,),daemon=True).start()
time.sleep(1)


from multiprocessing import Process,Value

def increment(shared_value):
    for i in range(100):
        with shared_value.get_lock():
            shared_value.value +=1

if __name__ =='__main__':
    num=Value('i',0)
    p1=Process(target=increment,args=(num,))
    p2=Process(target=increment,args=(num,))

    p1.start();p2.start()
    p1.join();p2.join()

    print(f'Final value: {num.value}')

import multiprocessing
import time

def worker(sema,worker_id):

    sema.acquire()
    print(f'Worker {worker_id} is working')
    time.sleep(2)
    print(f'Worker {worker_id} is done')
    sema.release()

if __name__ =='__main__':
    semaphore =multiprocessing.Semaphore(2)

    Process=[multiprocessing.Process(target=worker,args=(semaphore,i)) for i in range(5)]

    for p in Process : p.start()
    for p in Process : p.join()



import os

def child(pipeout):
    os.write("hello from child")
    os.close(pipeout)
def parent(pipein):
    pipein,pipeout=os.pipe()
    pid=os.fork()

    if pid==0:
        os.close(pipein)
        child(pipeout)
    else:
        os.close(pipeout)
        msg=os.read(pipein,1024)
        print(f"parent received: {msg.decode()}")
        os.close(pipein)
if __name__=='__main__':
    parent(None)"""

def banker_algorithm():
    # P0, P1, P2, P3, P4 are the names of Process

    n = 5  # Indicates the Number of processes
    r = 3  # Indicates the Number of resources
    alloc = [[0, 0, 1],  # P0 // This is Allocation Matrix
              [3, 0, 0],  # P1
              [1, 0, 1],  # P2
              [2, 3, 2],  # P3
              [0, 0, 3]]  # P4

    max_M = [[7, 6, 3],  # P0 // MAX Matrix
            [3, 2, 2],  # P1
            [8, 0, 2],  # P2
            [2, 1, 2],  # P3
            [5, 2, 3]]  # P4

    avail = [2, 3, 2]  # These are Available Resources

    f = [0] * n
    ans = [0] * n
    ind = 0
    need = [[0] * r for _ in range(n)]

    for i in range(n):
        for j in range(r):
            need[i][j] = max_M[i][j] - alloc[i][j]

    y = 0
    for k in range(n):
        for i in range(n):
            if f[i] == 0:
                flag = 0
                for j in range(r):
                    if need[i][j] > avail[j]:
                        flag = 1
                        break

                if flag == 0:
                    ans[ind] = i
                    ind += 1
                    for y in range(r):
                        avail[y] += alloc[i][y]
                    f[i] = 1

    print("The SAFE Sequence is as follows")
    for i in range(n - 1):
        print(f' P{ans[i]} ->', end='')
    print(f' P{ans[n - 1]}')

banker_algorithm()
