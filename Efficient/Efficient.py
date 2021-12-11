#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time
import tracemalloc
import sys

sys.path.append('../')
from sequenceAlignment import sequenceAlignment
from sequenceAlignmentEfficient import sequenceAlignmentEfficient

char2index = {'A':0 , 'C':1, 'G':2, 'T':3}
alphas = np.array([[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]], np.int32)
delta = 30

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

def calculateTime(string1, string2):
    total_time = 0
    start = time.time()
    Z, W, _ = sequenceAlignmentEfficient(string2,string1,alphas,delta)
    end = time.time()
    total_time += end-start

    return total_time

def calculateMemory(string1, string2):
    total_mem = 0
    tracemalloc.start()
    Z, W, _= sequenceAlignmentEfficient(string2,string1,alphas,delta)
    _ , peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_mem += peak_mem

    return total_mem

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
    numFiles = len(sys.argv)

    for i in range(1,numFiles):
        fileName = sys.argv[i]
        print(fileName)
        string1, string2 = readfile(fileName)

        Z, W, minScore = sequenceAlignmentEfficient(string2,string1,alphas,delta)

        average_time = calculateTime(string1, string2)
        average_memory = calculateMemory(string1, string2)
        
        output_filename = "output" + str(i) + ".txt"
        writeOutput(output_filename, Z, W, minScore, average_time, average_memory)  

if __name__ == "__main__":
    readinput()   





