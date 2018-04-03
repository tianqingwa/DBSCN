import pandas as pd
import numpy as np

import pylab as pl
import math
#read csv and return list
def readcsv():
    marks=pd.read_csv("/home/tsinghua/Desktop/go_track_trackspoints.csv")
    #print(marks)
    list=[]
    for index in marks.index:
        list.append((marks["latitude"][index],marks["longitude"][index]))
    return list
# acculate distance

def distance(p1,p2):
    lat1, lon1 = p1
    lat2, lon2 = p2
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def dbscan(D,e,m):
    # core T,k=0 cluster,c=[], unvisited p
    T=set()
    k=0
    C=[]
    P=set(D)
    for d in D:
        if( len([i for i in D if distance(d,i)<=e])>=m):
            T.add(d)
    # start cluster
    while len(T):
        p_old=P
        o=list(T)[np.random.randint(0, len(T))]
        P=P-set(o)
        Q=[]
        Q.append(o)
        while len(Q):
            q=Q[0]
            nq=[i for i in D if distance(q,i)<=e] #q :neigborhood
            if len(nq)>=m:
                S=P&set(nq)
                Q+=list(S)
                P=P-S
            Q.remove(q)
        k+=1
        Ck=list(p_old-P)
        T=T-set(Ck)
        C.append(Ck)

    print(k)
    return C

def draw(c):
    colvalue=['r', 'y', 'g', 'b', 'c', 'k', 'm']
    for i in range(len(c)):
        coo_x = []
        coo_y = []
        for j in range(len(c[i])):
            coo_x.append(c[i][j][0])
            coo_y.append(c[i][j][1])
        pl.scatter(coo_x, coo_y, marker='x', color=colvalue[i % len(colvalue)], label=i)
    pl.legend(loc='upper right')
    pl.show()
data = """
1,0.697,0.46,2,0.774,0.376,3,0.634,0.264,4,0.608,0.318,5,0.556,0.215,
6,0.403,0.237,7,0.481,0.149,8,0.437,0.211,9,0.666,0.091,10,0.243,0.267,
11,0.245,0.057,12,0.343,0.099,13,0.639,0.161,14,0.657,0.198,15,0.36,0.37,
16,0.593,0.042,17,0.719,0.103,18,0.359,0.188,19,0.339,0.241,20,0.282,0.257,
21,0.748,0.232,22,0.714,0.346,23,0.483,0.312,24,0.478,0.437,25,0.525,0.369,
26,0.751,0.489,27,0.532,0.472,28,0.473,0.376,29,0.725,0.445,30,0.446,0.459"""

a = data.split(',')
dataset = [(float(a[i]), float(a[i+1])) for i in range(1, len(a)-1, 3)]

#m=distance((-10.93934139,-37.06274211),(-10.93921056,-37.06284305))
#print m #test
d=readcsv()
#print(len(d))
C = dbscan(d, 0.1,20)
draw(C)

