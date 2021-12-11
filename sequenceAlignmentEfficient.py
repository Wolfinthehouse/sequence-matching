import numpy as np
import time
import tracemalloc

import sys

sys.path.append('../')
from sequenceAlignment import sequenceAlignment


char2index = {'A':0 , 'C':1, 'G':2, 'T':3}
alphas = np.array([[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]], np.int32)
delta = 30

def sequenceAlignmentEfficient(string1, string2, alphas, delta):
    minScoreList = []
    def NWScore(string1, string2, alphas, delta):
        m = len(string1)
        n = len(string2)
        
        lastline = [0 for i in range(n+1)]

        table = [[0 for i in range(n+2)] for j in range(2)]
        
        table[0][0] = 0

        for j in range(1,n+2):
            table[0][j] = table[0][j-1] + delta

        for i in range(1,m+1):
            table[1][0] = table[0][0] + delta
            for j in range(1,n+1):
                table[1][j] = min(table[0][j-1] + alphas[char2index[string1[i-1]]][char2index[string2[j-1]]] , table[0][j] + delta, table[1][j-1] + delta)
            table[0][:] = table[1][:]
            
        for j in range(n+1):
            lastline[j] = table[1][j]
        
        return lastline
    
    def PartitionY(scoreL,scoreR):
        zipped_lists = zip(scoreL, scoreR)
        sum_lists = [x + y for (x, y) in zipped_lists]
        return sum_lists.index(min(sum_lists)), min(sum_lists)
        
    def Hirschberg(string1,string2,alphas,delta):
        
        Z = ""
        W = ""
        m = len(string1)
        n = len(string2)
        
        if(m<=2 or n<=2):
            Z,W,minScore = sequenceAlignment(string1,string2,alphas,delta)
            minScoreList.append(minScore)
        else:
            string1len = m
            string1mid = m//2
            string2len = n
            
            scoreL = NWScore(string1[:string1mid],string2,alphas,delta)
            revString1 = string1[string1mid:]
            #print(revString1[::-1],string2[::-1])
            scoreR = NWScore(revString1[::-1],string2[::-1],alphas,delta)
            string2mid, minScore = PartitionY(scoreL,scoreR[::-1])
            minScoreList.append(minScore)
            #print(string2mid)
            
            Z1,W1 = Hirschberg(string1[:string1mid],string2[:string2mid],alphas,delta)
            Z2,W2 = Hirschberg(string1[string1mid:],string2[string2mid:],alphas,delta)
            Z = str(Z1) + str(Z2)
            W = str(W1) + str(W2)
        #print("Z: " + Z +"\n")
        #print("W: " + W +"\n")
                
        return Z,W
    Z, W = Hirschberg(string1,string2,alphas,delta)
    return Z, W, minScoreList[0]
