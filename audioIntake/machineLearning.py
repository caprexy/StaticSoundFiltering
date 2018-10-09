#https://stackoverflow.com/questions/42432850/how-to-create-my-own-datasets-using-in-scikit-learn
#features are data of samples
import pyaudio
import wave
import time
import sys
import struct
import csv
import os
import numpy as np
from sklearn.datasets.base import Bunch
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
import sklearn.naive_bayes
def wavToData(wavName):
    try:
        stream = wave.open("soundSamples\\point9SlicedMergedSamples\\%s"%wavName)
    except IOError:
        stream = wave.open("soundSamples\\point9TalkingSamples\\%s"%wavName)

    num_channels = stream.getnchannels()
    sample_rate = stream.getframerate()
    sample_width = stream.getsampwidth()
    num_frames = stream.getnframes()
    raw_data = stream.readframes( num_frames ) # Returns byte data
    stream.close()


    total_samples = num_frames * num_channels
    
    if sample_width == 1: 
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    integer_data = struct.unpack(fmt, raw_data) # this is amplitude

    return integer_data, num_frames, sample_rate  # int data contains both channels data


def dataMaker():
    endList = []
    for filename in os.listdir('C:\\Users\\School\\Documents\\GitHub\\StaticSoundFiltering\\audioIntake\\soundSamples\\point9SlicedMergedSamples\\'):
            if ".wav" in filename:
                    endList.append(filename)
    for filename in os.listdir('C:\\Users\\School\\Documents\\GitHub\\StaticSoundFiltering\\audioIntake\\soundSamples\\point9TalkingSamples\\'):
            if ".wav" in filename:
                    endList.append(filename)

    # does go in order so can grab each three. 1 sample is of either talking or megred and 3 samples (features, which is amplitude data)
    n_samples = 200 # 200 merged sounds
    n_features = 3 # the range of human hearing * 3 for each clip per sample

    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,), dtype=np.int)

    # builds the data list, which is features per 3 clips of the merged sounds
    x=0

    maxData = 0
    minData = 0
    
    while ( x != n_samples):
            file1 = endList.pop(0)  
            file2 = endList.pop(0)
            file3 = endList.pop(0)
            
            
            
            file1Data = wavToData(file1)[0]
            file2Data = wavToData(file2)[0]
            file3Data = wavToData(file3)[0]
                
            y=0

            #finds min and max
            while(y != len(file1Data)):
                data[x] += [file1Data[y],file2Data[y],file3Data[y]]
                if minData > min([file1Data[y],file2Data[y],file3Data[y]]):
                    minData = min([file1Data[y],file2Data[y],file3Data[y]])
                if maxData < max([[file1Data[y],file2Data[y],file3Data[y]]]):
                    maxData = max([file1Data[y],file2Data[y],file3Data[y]])
                y +=1

            # sets the target label, 0 if it is a talking data set, 1 if..         
            if(x > 100):
                    target[x] = np.asarray(0,dtype=np.int) # pure talk
            else:
                    target[x] = np.asarray(1,dtype=np.int)# sound
            x+=1

    # data normalization, failed to improve gnb but improved linearSVC a bit
    
    while x != len(data):
        array = data[x]
        for i in range(3):
            array[i] = (array[i]-minData)/(maxData-minData)
        x+=1
        
    
    data = shuffle(data,random_state = 400)
    target = shuffle(target,random_state = 400)
    data = Bunch(data=data,target=target)
    return data
print "linearsvc"
data = dataMaker()
train, test, train_targets, test_tagets = train_test_split(data.data, data.target, test_size = .33, random_state = 42)

model = LinearSVC(random_state = 0)
model.fit(train, train_targets)

predictions = model.predict(test)
print (accuracy_score(test_tagets, predictions))


print "gnb"
gnb = GaussianNB()
gnb.fit(train, train_targets)

predictions2 = gnb.predict(test)
print (accuracy_score(test_tagets, predictions2))
##
##from sklearn.svm import SVC
##svc =SVC(gamma="auto")
##clf.fit(train,train_targets)
##clf.predict(test)
##print clf.score(test,test_tagets)

