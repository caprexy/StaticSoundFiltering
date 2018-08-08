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

def wavToData(wavName):
    try:
        stream = wave.open("point9SlicedMergedSamples\\%s"%wavName)
    except IOError:
        stream = wave.open("puretalking\\%s"%wavName)

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

endList = []
for filename in os.listdir('C:\\Users\\School\\Documents\\GitHub\\StaticSoundFiltering\\audioIntake\\soundSamples\\point9SlicedMergedSamples\\'):
    if ".wav" in filename:
        endList.append(filename)
for filename in os.listdir('C:\\Users\\School\\Documents\\GitHub\\StaticSoundFiltering\\audioIntake\\soundSamples\\puretalking\\'):
    if ".wav" in filename:
        endList.append(filename)

# does go in order so can grab each three
n_samples = 200 # 100 merged sounds
n_features = 3 # the range of human hearing * 3 for each clip per sample

data = np.empty((n_samples, n_features))
target = np.empty((n_samples,), dtype=np.int)

# builds the data list, which is features per 3 clips of the merged sounds
x=0
print len(endList)

while ( x != n_samples):
    file1 = endList.pop(0)
    file2 = endList.pop(0)
    file3 = endList.pop(0)
    
    print len(endList)
    
    file1Data = wavToData(file1)[0]
    file2Data = wavToData(file2)[0]
    file3Data = wavToData(file3)[0]

    y=0
    while(y != len(file1Data)):
          data[x] += [file1Data[y],file2Data[y],file3Data[y]]
          y +=1
          
    x+=1

 # need to add correct data



