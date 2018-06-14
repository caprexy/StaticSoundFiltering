import pyaudio
import wave
import sys
import numpy as np
import struct
import random

def init():
	#Handles all tasks that must be done on program start

	#Initialize singleton PyAudio object
	global p
	p = pyaudio.PyAudio()

def openStream():
	#This method opens and returns an audio stream of standardized format
	return p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

def recordForTime(stream, seconds):
	#Returns an array of audio chunks
	frames = []

	for i in range(0, int(44100/1024*seconds)):
		data = stream.read(1024)
		frames.append(data)
	
	return frames

def closeStream(stream):
	#Close the passed in stream
	stream.stop_stream()
	stream.close()

def writeToFile(filename, frames):
	#Write the frames array to a wav file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(1)
	wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
	wf.setframerate(44100)
	wf.writeframes(b''.join(frames))
	wf.close()

def openFile(filename):
	#Opens the file specified in bytewise read mode
	return open(filename,'rb')

def readFile(fn):
	#Read the literal bytes of a file and returns an array of integers corresponding to it's information
	ret = {}
	sound_file = wave.open(fn, 'r')
	file_length = sound_file.getnframes()
	data = sound_file.readframes(file_length)
	sound_file.close()
	data = struct.unpack('{n}h'.format(n=file_length), data)
	sound = np.array(data)
	return sound
#	i = 0
#	try:
#		byte = fh.read(1)
#		byte2 = fh.read(1)
#		while byte != "" and byte2 != "":
#			ret[i] = (ord(byte) & 0xffff) + (ord(byte2) & 0xff)
#			i += 1
			#if (ord(byte) & 0x01) is 0x01:
			#	print 1
			#else:
			#	print 0
#			byte = fh.read(1)
#			byte2 = fh.read(1)
#	finally:
#		fh.close()

def exit():
	#Handle all tasks to be done on program exit
	p.terminate()

def printToPlot(audioIn):
	sys.stdout.write("Frequency,")
	ii = 0
	for i in audioIn:
		sys.stdout.write(str(ii)+",")
		ii += 1
	sys.stdout.write("Amplitude")
	for i in audioIn:
		sys.stdout.write(","+str(i))
	sys.stdout.flush()
	exit()

def wavToArray(fname):
	wf = wave.open(fname, 'rb')
	return wf.readframes(wf.getnframes())	

def arrayToWav(array, fname):
	wf = wave.open(fname, 'wb')
	wf.setnchannels(2)
	wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
	wf.setframerate(44100)
	frames = []
	for i in array:
		frames.append(str(i))
	wf.writeframes(b''.join(frames))
	wf.close()

def main():
	#Run program
	init()
	stream = openStream()
	#print recordForTime(stream, 0.024)
	writeToFile("test.wav", recordForTime(stream, int(sys.argv[1])))#0.00022675737)) <- This should write exactly 1 byte of recording (I think uncertainty means this ends up writing 0)
	closeStream(stream)
	audioIn = readFile("test.wav")
	#print audioIn
	printToPlot(audioIn)
	print "Running array to wave"
	arrayToWav(audioIn,'temp.wav')
	print "finished writing to temp.wav"
	exit()

def bandPass(data,minFreq,maxFreq):
	filteredData = [] # x val is freq, y val is ampltiude. 1-255
	curFreq = 1
	while(curFreq <= maxFreq):
		print curFreq
 		if(curFreq >= minFreq):
			filteredData.append(data[curFreq-1])
		else:
			filteredData.append(0)
		curFreq = curFreq + 1
	#print filteredData
	return scipy.fft.irfft(filteredData)

def toCsv():
	init()
	arr = []
	for i in range(599999):
		arr.append(random.randint(-128,127))
	arrayToWav(arr,'log.wav')
	arr = wavToArray('playback.wav')
	printToPlot(arr)
	printToPlot(bandPass(arr,85,255))
	exit()

#main()

toCsv()