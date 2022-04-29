import csv, random, math
from scipy.optimize import minimize, curve_fit
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

#Reading in Data
year = input("Enter a year:")
dataDict = {}
genreDict = []

lineDictOverall = {}
with open('data/vgsales.csv') as csvfile:

    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        if row[3] == 'N/A': 

            next(reader)
        else:

            csvYear = int(row[3])
            #General Line Graph 
            if (csvYear in lineDictOverall.keys()):
                
                lineDictOverall[csvYear] += float(row[10])
            
            else:

                lineDictOverall[csvYear] = float(row[10])

def rootMinSquare(actuY, dataY):

    rms_error = 0
    sum_diff_square = 0
    for y1, y2 in zip(actuY, dataY):

        diff = y2-y1
        sum_diff_square += diff * diff

    rms_error=math.sqrt(sum_diff_square)/len(actuY)
    return rms_error

def getNextVal(rms1, rms2, multiplyval):

    if rms1 > rms2:

        multiplyval += -0.5
    else:

        multiplyval -= 0.5
    
    return multiplyval

def curveExpFunc(x, a, b, c):

    return a ** (b * np.log(x) + c)


#Create the graph subplot 
fig, graph = plt.subplots(2)


#Curve fit
OverallGameSales = OrderedDict(sorted(lineDictOverall.items()))

SalesX = np.array(list(OverallGameSales.keys()))
SalesY = np.array(list(OverallGameSales.values()))
SalesXTill2008 = np.array([])
SalesYTill2008 = np.array([])

iterator = 0
while SalesX[iterator] <= 2008:

    SalesXTill2008 = np.concatenate((SalesXTill2008, [SalesX[iterator]]))
    SalesYTill2008 = np.concatenate((SalesYTill2008, [SalesY[iterator]]))   
    iterator += 1

popt, pcov = curve_fit(curveExpFunc, SalesXTill2008, SalesYTill2008)
graph[0].plot(SalesXTill2008, curveExpFunc(SalesXTill2008, *popt), 'red')
graph[0].plot(SalesXTill2008, SalesYTill2008, 'blue')

print(rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, *popt)))

#Creating our own curve_fit function
initA = SalesYTill2008[0]
initB = 1
initC = 1

addValA = 4.0
addValB = 4.0
addValC = 4.0

aWhile = True
bWhile = True
cWhile = True
while aWhile:

    addValA = getNextVal(rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)), rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA + addValA, initB, initC)), addValA)
    initA += addValA

    if rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)) < 100:

        aWhile = False

    while bWhile:

        addValB = getNextVal(rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)), rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB + addValB, initC)), addValB)
        initB += addValB

        if rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)) < 100:

            bWhile = False

        while cWhile:

            addValC = getNextVal(rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)), rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC + addValC)), addValC)
            initC += addValC

            if rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)) < 100:

                cWhile = False

print(rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC)))
print(initA, initB, initC)
graph[1].plot(SalesXTill2008, curveExpFunc(SalesXTill2008, initA, initB, initC), 'green')
#Show the graph
plt.show()