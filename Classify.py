import numpy as np
import pickle
from sklearn import neighbors, datasets
from numpy.core import multiarray

train0 = pickle.load(open('userData/train0.dat','rb'))
train1 = pickle.load(open('userData/train1.dat','rb'))
train2 = pickle.load(open('userData/train2 (3).dat','rb'))
train3 = pickle.load(open('userData/train3 (3).dat','rb'))
train4 = pickle.load(open('userData/train4 (2).dat','rb'))
train5 = pickle.load(open('userData/train5.dat','rb'))
train6 = pickle.load(open('userData/train6 (2).dat','rb'))
train7 = pickle.load(open('userData/train7 (5).dat','rb'))
train8 = pickle.load(open('userData/train8 (5).dat','rb'))
train9 = pickle.load(open('userData/train9.dat','rb'))

test0 = pickle.load(open('userData/test0.dat','rb'))
test1 = pickle.load(open('userData/test1.dat','rb'))
test2 = pickle.load(open('userData/test2 (3).dat','rb'))
test3 = pickle.load(open('userData/test3 (3).dat','rb'))
test4 = pickle.load(open('userData/test4 (2).dat','rb'))
test5 = pickle.load(open('userData/test5.dat','rb'))
test6 = pickle.load(open('userData/test6 (2).dat','rb'))
test7 = pickle.load(open('userData/test7 (5).dat','rb'))
test8 = pickle.load(open('userData/test8 (5).dat','rb'))
test9 = pickle.load(open('userData/test9.dat','rb'))


def ReshapeData(set1,set2,set3,set4,set5,set6,set7,set8,set9,set10):
    X = np.zeros((10000,5*2*3),dtype='f')
    y = np.zeros(10000)
    for i in range(0,1000):
        n = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    X[i,n] = set1[j,k,m,i]
                    y[i] = 5
                    X[i+1000,n] = set2[j,k,m,i]
                    y[i+1000] = 0
                    X[i+2000,n] = set3[j,k,m,i]
                    y[i+2000] = 1
                    X[i+3000,n] = set4[j,k,m,i]
                    y[i+3000] = 2
                    X[i+4000,n] = set5[j,k,m,i]
                    y[i+4000] = 3
                    X[i+5000,n] = set6[j,k,m,i]
                    y[i+5000] = 4
                    X[i+6000,n] = set7[j,k,m,i]
                    y[i+6000] = 6
                    X[i+7000,n] = set8[j,k,m,i]
                    y[i+7000] = 7
                    X[i+8000,n] = set9[j,k,m,i]
                    y[i+8000] = 8
                    X[i+9000,n] = set9[j,k,m,i]
                    y[i+9000] = 9
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
    
    allyCoordinates = X[:,:,1,:]
    meanValue = allyCoordinates.mean()
    X[:,:,1,:] = allyCoordinates - meanValue
    
    allzCoordinates = X[:,:,2,:]
    meanValue = allzCoordinates.mean()
    X[:,:,2,:] = allzCoordinates - meanValue
    
    return X

train5 = ReduceData(train5)
test5 = ReduceData(test5)
train0 = ReduceData(train0)
test0 = ReduceData(test0)
train1 = ReduceData(train1)
test1 = ReduceData(test1)
train2 = ReduceData(train2)
test2 = ReduceData(test2)
train3 = ReduceData(train3)
test3 = ReduceData(test3)
train4 = ReduceData(train4)
test4 = ReduceData(test4)
train6 = ReduceData(train6)
test6 = ReduceData(test6)
train7 = ReduceData(train7)
test7 = ReduceData(test7)
train8 = ReduceData(train8)
test8 = ReduceData(test8)
train9 = ReduceData(train9)
test9 = ReduceData(test9)

train5 = CenterData(train5)
test5 = CenterData(test5)
train0 = CenterData(train0)
test0 = CenterData(test0)
train1 = CenterData(train1)
test1 = CenterData(test1)
train2 = CenterData(train2)
test2 = CenterData(test2)
train3 = CenterData(train3)
test3 = CenterData(test3)
train4 = CenterData(train4)
test4 = CenterData(test4)
train6 = CenterData(train6)
test6 = CenterData(test6)
train7 = CenterData(train7)
test7 = CenterData(test7)
train8 = CenterData(train8)
test8 = CenterData(test8)
train9 = CenterData(train9)
test9 = CenterData(test9)


trainX,trainy = ReshapeData(train5,train0,train1,train2,train3,train4,train6,train7,train8,train9)
testX,testy = ReshapeData(train5,train0,train1,train2,train3,train4,train6,train7,train8,train9)
 
clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)


counter = 0
for i in range(0,2000):
    actual = int(testy[i])
    prediction = int(clf.predict([testX[i,:]]))
    if(prediction == actual):
        counter += 1
print (counter/2000.0)*100



# print testX,testy
# print testX.shape,testy.shape

pickle.dump(clf, open('userData/classifier.p','wb'))