import csv, random, math
from scipy.optimize import minimize, curve_fit
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

#Reading in Data
year = input("Enter a year:")
dataDict = {}
genreDict = []

lineDictAction = {}
lineDictOverall = {}
with open('data/vgsales.csv') as csvfile:

    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        if row[3] == 'N/A': 

            next(reader)
        else:

            csvYear = int(row[3])
            #Bar Graph
            if csvYear == int(year):
                
                genre = row[4]
                globalSales = float(row[10])

                if (genre in dataDict.keys()):
                    
                    dataDict[genre] += globalSales

                else:

                    dataDict[genre] = int(globalSales) 
                    genreDict.append(str(genre))   
            
            #Action Line Graph
            if (row[4] == 'Action'):

                if (csvYear in lineDictAction.keys()):
                    
                    lineDictAction[csvYear] += float(row[10])

                else:

                    lineDictAction[csvYear] = float(row[10])

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

#Create the graph subplot 
fig, graph = plt.subplots(4)

#Bar Graph
barX = []
barY = []
for i in range(len(genreDict)):

    barX.append(genreDict[i])
    barY.append(dataDict[genreDict[i]])

graph[0].bar(barX, barY)

#Line Graph for action and total sales over course of years of given data
ActionGameSales = OrderedDict(sorted(lineDictAction.items()))
OverallGameSales = OrderedDict(sorted(lineDictOverall.items()))

graph[1].plot(ActionGameSales.keys(), ActionGameSales.values(), 'yellow')
graph[1].plot(OverallGameSales.keys(), OverallGameSales.values(), 'red')

#Exponential Graph
expoX = np.arange(-20, 20, 0.25, dtype = float)
expoY = []

for i in expoX:

    expoY.append(np.exp(i))

graph[2].plot(expoX, expoY)

#Curve fit

def curveExpFunc(x, a, b, c):
    
    return a ** (b * x + c)

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
graph[3].plot(SalesXTill2008, curveExpFunc(SalesXTill2008, *popt), 'red')
graph[3].plot(SalesXTill2008, SalesYTill2008, 'blue')

print(rootMinSquare(SalesYTill2008, curveExpFunc(SalesXTill2008, *popt)))

#Creating our own curve_fit function



#Show the graph
plt.show()