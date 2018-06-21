import pyaudio
import wave
import time
import sys
import struct
import csv



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

    integer_data = struct.unpack(fmt, raw_data) 
    return integer_data, num_frames, sample_rate

def dataToWav(wavName,data):
    # IMPORTANT hard coded standard values, refenced from the audiocheck.net files
    stream = wave.open(wavName,"wb")
    stream.setnchannels(1)
    stream.setframerate(44100)
    stream.setsampwidth(2)
    stream.setnframes(132301)
    fmt = "%ih" % 132301*1 
        
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
    
wavToCsv('audiocheck.net_sin_4000Hz_-3dBFS_3s.wav','4000hz.csv')
#include tags (.wav/.csv)
