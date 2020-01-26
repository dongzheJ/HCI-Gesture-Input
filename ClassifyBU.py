import numpy as np
import pickle
from sklearn import neighbors, datasets

fileName = 'userData/train5.dat'
fileName1 = 'userData/train0.dat'
fileName2 = 'userData/test5.dat'
fileName3 = 'userData/test0.dat'

f = open(fileName,'rb')
f1 = open(fileName1,'rb')
f2 = open(fileName2,'rb')
f3 = open(fileName3,'rb')

trainM = pickle.load(f)
trainN = pickle.load(f1)
testM = pickle.load(f2)
testN = pickle.load(f3)

def ReshapeData(set1,set2):
    X = np.zeros((2000,5*4*6),dtype='f')
    y = np.zeros((2000,5*4*6),dtype='f')
    for i in range(0,1000):
        n = 0
        for j in range(0,5):
            for k in range(0,4):
                for m in range(0,6):
                    X[i,n] = set1[j,k,m,i]
                    y[i] = 5
                    y[i+1000] = 0
                    n = n + 1
    return X,y

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X
    
def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue
    
    allyCoordinates = X[:,0,:,:]
    meanValue = allyCoordinates.mean()
    X[:,:,0,:] = allyCoordinates - meanValue
    
    allzCoordinates = X[:,:,:,0]
    meanValue = allzCoordinates.mean()
    X[:,:,0,:] = allzCoordinates - meanValue
    
    return X

# trainM = ReduceData(trainM)
# trainN = ReduceData(trainN)
# trainM = ReduceData(testM)
# trainN = ReduceData(testN)
# 
# trainM = CenterData(trainM)
# trainN = CenterData(trainN)
# trainM = CenterData(testM)
# trainN = CenterData(testN)

trainX,trainy = ReshapeData(trainM,trainN)
testX,testy = ReshapeData(testM,testN)

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)


counter = 0
for i in range(0,2000):
    actual = testy[i]
    prediction = clf.predict([testX[i,:]])
    if(prediction.any() == actual.any()):
        counter+=1
print (counter/2000.0)*100

# print trainX,trainy
# print trainX.shape,trainy.shape