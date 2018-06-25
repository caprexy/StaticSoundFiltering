import pyaudio
import wave
import time
import sys
import struct
import csv

# all files and stuffs need to contain their tags ('potatos.wav')

def wavToData(wavName):
    stream = wave.open(wavName)

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
    return integer_data, num_frames, sample_rate 

def dataToWav(wavName,data):
    # IMPORTANT hard coded standard values, refenced from the audiocheck.net files
    stream = wave.open(wavName,"wb")
    stream.setnchannels(1)
    stream.setframerate(44100)
    stream.setsampwidth(2)
    numFrames = len(data)
    stream.setnframes(numFrames)
    fmt = "%ih" % numFrames 

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
    
    limitCheck = lambda x,y: ((x+y)> 32767 or (x+y) < -32767)
    limitConstrain = lambda x,y: 32767 if (x+y) >32767 else -32767
    newData = []

    if len(firstData) < len(secondData): #adds the amplitudes of both wav file up to the shortest one
        for i in range(len(firstData)):
            data = 0
            if(limitCheck(firstData[i],secondData[i])): #exceed limit
               data = limitConstrain(firstData[i],secondData[i])
            else:
               data = firstData[i]+secondData[i]
            
            newData.append(data)
            
    else:
        for i in range(len(secondData)):
            data = 0
            if(limitCheck(firstData[i],secondData[i])): #exceed limit
               data = limitConstrain(firstData[i],secondData[i])
               
            else:
               data = firstData[i]+secondData[i]
               
               if (data > 32767 or data <-32767):
                 print data
            newData.append(data)


    dataToWav(mergeWav,newData)

mergeWavData('audiocheck.net_sin_1000Hz_-3dBFS_3s.wav','audiocheck.net_sin_4000Hz_-3dBFS_3s.wav','1000Hz+4000Hz.wav')
wavToCsv('1000Hz+4000Hz.wav','1000Hz+4000Hz.csv') # maeks csv out of wav ayayayay
#include tags (.wav/.csv)
