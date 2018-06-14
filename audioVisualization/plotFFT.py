# takes in an iput of csv: xName, x vals.... ,yName, y vals....
import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import csv
import scipy
from scipy.fftpack import rfft

class Main(QMainWindow):
    
    def __init__(self):
        super(Main,self).__init__()
        self.ui = uic.loadUi('plotData.ui', self)
        self.xVals = []
        self.yVals = []
        self.flipAxis = True
        self.readVals('testFile.csv') # CHANGE MY NAME FROM TEST.CSV TO UR FILE
        fft = scipy.fftpack.rfft(self.yVals)
        for i in fft:
            sys.stdout.write(str(i)+",")
        self.ui.plotWidget.plot(self.xVals,scipy.fftpack.rfft(self.yVals),pen = (1,3))
                
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

                    
            
                    
        
            

def main():
    app = QApplication(sys.argv)
    instance = Main()
    instance.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
