#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time
import tracemalloc


# In[2]:


def readfile(file):
    with open(file) as f:
        contents =  f.readlines()
        
    testcases = []
    case = []
    for line in contents:
        word = line.split('\n')[0]
        if word.isalpha():
            testcases.append(case)
            case = []
            case.append(word)
        else:
            case.append(word)
    testcases.append(case)
    testcases.pop(0)
    
    finalStrings = []
    for case in testcases:
        baseString = ""
        for index in range(len(case)):
            if index==0:
                baseString = case[index]
            else:
                baseString = baseString[0:int(case[index])+1] +  baseString + baseString[int(case[index])+1:]
        finalStrings.append(baseString)
    return finalStrings[0], finalStrings[1]


char2index = {'A':0 , 'C':1, 'G':2, 'T':3}
alphas = np.array([[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]], np.int32)

delta = 30

def sequenceAlignment(string1, string2, alphas, delta):
    m = len(string1)
    n = len(string2)
    
    table = [[0 for i in range(n+2)] for i in range(m+2)]

    for i in range(n+2):
        table[0][i] = i*delta
    for j in range(m+2):
        table[j][0] = j*delta   
    #print(table)
    
    for i in range(1,m+1):
        for j in range(1,n+1):
            if(string1[i-1]==string2[j-1]):
                table[i][j] = table[i-1][j-1]
            else:
                table[i][j] = min(table[i-1][j-1] + alphas[char2index[string1[i-1]]][char2index[string2[j-1]]] , table[i-1][j] + delta, table[i][j-1] + delta)
                
    #print(table)
    
    l = m + n
    
    string1pos = l
    string2pos = l
    
    string1ans = [0 for i in range(l+1)]
    string2ans = [0 for i in range(l+1)]
        
    i = m 
    j = n
        
    while(not(i==0 or j==0)):
        if(string1[i-1] == string2[j-1]):
            string1ans[string1pos] = string1[i-1]
            string1pos -= 1
            string2ans[string2pos] = string2[j-1]
            string2pos -= 1
            i-=1
            j-=1
        elif(table[i-1][j-1] + alphas[char2index[string1[i-1]]][char2index[string2[j-1]]] == table[i][j]):
            string1ans[string1pos] = string1[i-1]
            string1pos -= 1
            string2ans[string2pos] = string2[j-1]
            string2pos -= 1
            i-=1
            j-=1
        elif(table[i-1][j] + delta == table[i][j]):
            string1ans[string1pos] = string1[i-1]
            string1pos -= 1
            string2ans[string2pos] = '_'
            string2pos -= 1
            i-=1
        elif(table[i][j-1] + delta == table[i][j]):
            string1ans[string1pos] = '_'
            string1pos -= 1
            string2ans[string2pos] = string2[j-1]
            string2pos -= 1
            j-=1
            
    while(string1pos>0):
        if(i>0):
            i -= 1
            string1ans[string1pos] = string1[i]
            string1pos -= 1
        else:
            string1ans[string1pos] = '_'
            string1pos -= 1
    
    while(string2pos>0):
        if(j>0):
            j -= 1
            string2ans[string2pos] = string2[j]
            string2pos -= 1
        else:
            string2ans[string2pos] = '_'
            string2pos -= 1
            
    idd = 1
    
    for i in range(l,0,-1):
        if(string2ans[i] == '_' and string1ans[i] == '_'):
            idd = i + 1
            break
        
    #print("Min Penalty : " + str(table[m][n]))
    
    finalString1,finalString2 = [], []
    for i in range(idd,l+1):
        #print(string1ans[i],end='')
        finalString1.append(string1ans[i])
    #print("")
    
    for i in range(idd,l+1):
        #print(string2ans[i],end='')
        finalString2.append(string2ans[i])
    #print("")
    
    return ('').join(finalString1),('').join(finalString2), table[m][n]


# In[7]:


minScoreList = []


# In[8]:


def sequenceAlignmentEfficient(string1, string2, alphas, delta):
    
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
    return Hirschberg(string1,string2,alphas,delta)


# In[21]:


tracemalloc.start()
start = time.time()
Z, W = sequenceAlignmentEfficient(string2,string1,alphas,delta)
end = time.time()
# print(Z[:50])
# print(Z[-50:])
# print(W[:50])
# print(W[-50:])
first_size, first_peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(Z)
print(W)
print(minScoreList[0])
print(end-start)
print(first_peak)


def 





