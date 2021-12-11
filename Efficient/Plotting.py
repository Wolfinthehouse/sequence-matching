import numpy as np
import time
import tracemalloc
import matplotlib.pyplot as plt
import os

import sys

sys.path.append('../')
from sequenceAlignmentEfficient import sequenceAlignmentEfficient

char2index = {'A':0 , 'C':1, 'G':2, 'T':3}
alphas = np.array([[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]], np.int32)
delta = 30

def readfile(file):
    with open(os.path.join("../Inputs", file)) as f:
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

def calculateTime(string1, string2):
    total_time = 0
    for i in range(20):
        start = time.time()
        Z, W, minScore = sequenceAlignmentEfficient(string2,string1,alphas,delta)
        end = time.time()
        total_time += end-start
    return total_time/20

def calculateMemory(string1, string2):
    total_mem = 0
    for i in range(20):
        tracemalloc.start()
        Z, W, minScore = sequenceAlignmentEfficient(string2,string1,alphas,delta)
        _ , peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_mem += peak_mem
    return total_mem/20


def writeOutput(output_filename, Z, W, minScore, average_time, average_memory):
    with open(output_filename, "w") as f:
        print(output_filename)
        f.write(Z[:50])
        f.write(" ")
        f.write(Z[-50:])
        f.write("\n")
        f.write(W[:50])
        f.write(" ")
        f.write(W[-50:])
        f.write("\n")
        f.write(str(minScore))
        f.write("\n")
        f.write(str(average_time))
        f.write("\n")
        f.write(str(average_memory))
        f.write("\n")
    

def readinput():
    time = []
    memory = []
    size = []

    for fileName in os.listdir(sys.argv[1]):
        print(fileName)
        string1, string2 = readfile(fileName)

        #Z, W, minScore = sequenceAlignment(string2,string1,alphas,delta)

        average_time = calculateTime(string1, string2)
        average_memory = calculateMemory(string1, string2)

        time.append(average_time)
        memory.append(average_memory/1024)
        size.append(len(string1)+len(string2))


    print(size)
    print(time)
    print(memory)
    new_size, new_time = zip(*sorted(zip(size, time)))
    new_size2, new_memory = zip(*sorted(zip(size, memory)))
    plt.figure()
    plt.subplot(211)
    plt.xlabel("Input Size")
    plt.ylabel("CPU Time(Seconds)")
    plt.plot(new_size,new_time)
    
    plt.subplot(212)
    plt.xlabel("Input Size")
    plt.ylabel("Memory(KB)")
    plt.plot(new_size2,new_memory)
    plt.show()
        # output_filename = "output" + str(i) + ".txt"
        # writeOutput(output_filename, Z, W, minScore, average_time, average_memory)  

if __name__ == "__main__":
    readinput()   




