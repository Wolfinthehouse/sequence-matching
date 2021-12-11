import numpy as np
import time
import tracemalloc

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

