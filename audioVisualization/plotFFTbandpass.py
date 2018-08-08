# takes in an iput of csv: xName, x vals.... ,yName, y vals....
import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import csv
import scipy
from scipy.fftpack import rfft
from scipy.fftpack import irfft

class Main(QMainWindow):
    
    def __init__(self):
        super(Main,self).__init__()
        self.ui = uic.loadUi('plotData.ui', self)
        self.xVals = []
        self.yVals = []
        self.flipAxis = True
        self.readVals('testFile.csv') # CHANGE MY NAME FROM TEST.CSV TO UR FILE
        fft = scipy.fftpack.rfft(self.yVals)
        self.newList = []
        i = 0
        while i != 255:
            self.newList.append(i)
            i = i+1
        self.ui.plotWidget.plot(self.newList,self.bandPass(fft,85,255),pen = (1,3))
                
        # to look closer you can use right click
        #then drag left or right or up and down
    def readVals(self, csvName):
        with open(csvName, 'rb') as csvfile:
            reader = csv.reader(csvfile, quotechar = '|')
            for item in reader:
                while len(item) != 0:
                    try:
                        int(item[0])
                        if self.flipAxis == False:
                            self.xVals.append(int(item.pop(0)))
                        else:
                            self.yVals.append(int(item.pop(0)))
                    except:
                        if self.flipAxis == False:
                            self.label_2.setText(item.pop(0))
                        else:
                            self.label.setText(item.pop(0))
                        self.flipAxis = not self.flipAxis
            if len(self.xVals) != len(self.yVals):
                if (self.yVals > self.xVals):
                    while len(self.xVals) != len(self.yVals):
                        self.xVals.append((self.xVals[-1]+1))

            
    # 85-255
    def bandPass(self,data,minFreq,maxFreq):
            filteredData = [] # x val is freq, y val is ampltiude. 1-255
            curFreq = 1
            while(curFreq <= maxFreq):
                    if(curFreq >= minFreq):
                            filteredData.append(data[curFreq-1])
                    else:
                            filteredData.append(0)
                    curFreq = curFreq + 1
            
            return filteredData
            #return scipy.fft.irfft(filteredData)

            
                    
        
            

def main():
    app = QApplication(sys.argv)
    instance = Main()
    instance.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
