import csv
from scipy.fftpack import rfft
#low pass filter into inverse filter
# x vals are just the freq number

# 85-255
def bandPass(data,minFreq,maxFreq):
	filteredData = [] # x val is freq, y val is ampltiude. 1-255
	curFreq = 1
	while(curFreq <= maxFreq):
 		if(curFreq >= minFreq):
			filteredData.append(data[curFreq-1])
		else:
			filteredData.append(0)
		curFreq = curFreq + 1

	print filteredData
	return scipy.fft.irfft(filteredData)