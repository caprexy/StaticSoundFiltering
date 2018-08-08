import pyaudio
import wave
import time
import sys
import struct
import csv
import os

# to cut audio

def wavToData(wavName): #simple wav to data
    print wavName
    stream = wave.open(wavName) #formatting?

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
        
    total_samples = num_frames * num_channels

    integer_data = struct.unpack(fmt, raw_data) # this is amplitude
    return integer_data, num_frames,

def cutter(wavName, cutLength, numCut): # name, seconds of cut, number of cuts
    data, num_Frames = wavToData(wavName)
    stream = wave.open(wavName)
    numFrames = int(stream.getframerate()*cutLength) # a cutLength
    x = 0
    while(x != numCut):
        new = wave.open(wavName + "Cut%f"%x+".wav","wb")
        new.setnchannels(1)
        new.setframerate(44100)
        new.setsampwidth(2)
        slicedData = data[0:numFrames]
        data = data[numFrames:-1]
        fmt = "%ih" % numFrames 
        packingData = struct.pack(fmt,*slicedData)
        new.writeframes(packingData)
        x+=1
        new.close()

#cutter("carRideo (1).wav",.9,3)
##endList = []
##for filename in os.listdir('C:\\Users\\School\\Documents\\GitHub\\StaticSoundFiltering\\audioIntake\\soundSamples\\point9SlicedMergedSamples\\'):
##    if ".wav" in filename:
##        endList.append(filename)
##        
##for i in endList:
##    cutter(i,.45,2)

cutter("RHCXX7vA2QY (3).wav",.9, 300)
