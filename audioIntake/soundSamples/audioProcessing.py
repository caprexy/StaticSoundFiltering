import pyaudio
import wave
import time
import sys
import struct
import csv
import os

# all files and stuffs need to contain their tags ('potatos.wav')

def wavToData(wavName):
    stream = wave.open("pureTalk\\%s"%wavName)

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

def dataToWav(wavName,data):
    # IMPORTANT hard coded standard values, refenced from the audiocheck.net files
    stream = wave.open(wavName,"wb")
    stream.setnchannels(2)
    stream.setframerate(44100)
    stream.setsampwidth(2)
    totalSamples = len(data)

    stream.setnframes(totalSamples/2)
    fmt = "%ih" % totalSamples
    data = struct.pack(fmt,*data) #unpacks all
    stream.writeframes(data)

    
def wavToCsv(wavName,csvName): 
    with open(csvName, 'wb') as csvfile: #contain all data in 1 row
                                                # x = time (1 frame)
                                                # y = freq
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        #get data
        integer_data, num_frames, sample_rate = wavToData(wavName)
        #adds headings and other needed data
        frameCount = [x+1 for x in range(num_frames)] # x
        fullData = [x for x in integer_data] # y
        frameCount.insert(0, "Time (increments of %f)"%(1/sample_rate))
        fullData.insert(0,"Frequency(dBfs)")
        fullData = frameCount+fullData
        filewriter.writerow(fullData)

def mergeWavData(wav1,wav2,mergeWav): #generates a brand new wav file
    firstData = wavToData(wav1)[0]
    secondData = wavToData(wav2)[0]
    newData = []
    if len(firstData) < len(secondData): #adds the amplitudes of both wav file up to the shortest one
        for i in range(len(firstData)):
            data = firstData[i]+secondData[i] 
            newData.append(data)
    else:
        for i in range(len(secondData)):
            data = firstData[i]+secondData[i] 
            newData.append(data)
    while(max(newData) > 32767 or min(newData) < -32767):
        newData = [i/2 for i in newData]
    dataToWav(mergeWav,newData)

#mergeWavData('carDrive.wav','carRideo (1).wav','fan+4000hz.wav')
#wavToCsv('1000Hz+4000Hz.wav','1000Hz+4000Hz.csv') # maeks csv out of wav ayayayay
#include tags (.wav/.csv)

talkingList = [] # seperates sounds
otherList = []
for filename in os.listdir("C:\\Users\\School\\Documents\\GitHub\\StaticSoundFiltering\\audioIntake\\soundSamples\\pureTalk"):
    if ".wav" in filename:
        filename = filename[:-4]
	#seperate talking and non talking
        if "talking" in filename:
            talkingList.append(filename)
        else:
            otherList.append(filename)

for i in talkingList:
    for b in otherList:
        mergeWavData(i+".wav",b+".wav",i + " " + b + ".wav")


