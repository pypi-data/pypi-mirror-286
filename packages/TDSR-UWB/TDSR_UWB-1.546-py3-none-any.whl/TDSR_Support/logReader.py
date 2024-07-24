from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QComboBox, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
import sys  # We need sys so that we can pass argv to QApplication
import json
from pathlib import Path

__version__ = "1.546"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.logDir = "../../../LogFiles/Ambit/"
        self.logPath = Path(self.logDir)
        if self.logPath.is_dir() == True:
            self.filename = QFileDialog.getOpenFileName(self, 'Open Requester File', self.logDir, 'Logs (*.log *.json)')
        else:
            self.filename = QFileDialog.getOpenFileName(self, 'Open Requester File', "./", 'Logs (*.log *.json)')
        # print("FileName:", self.filename[0])
        self.mainWindowSheet = "QMainWindow {background-color: rgb(100,160,220);}"
        self.setWindowTitle("Ambit Radio LogFile Viewer")
        self.setStyleSheet(self.mainWindowSheet)
        self.graphSizeX = 1400
        self.graphSizeY = 1000
        self.dataStart = 5
        self.dataStop = 5000
        self.dropMenuOptions = []
        self.setGeometry(10,10,self.graphSizeX+5,self.graphSizeY+100)
        self.initGUI()
        self.readFileData()
        self.show()


    def readFileData(self):
        logfile = open(self.filename[0],"r")
        dataLines = logfile.readlines()
        self.dispDataTotal.setText(str(len(dataLines)))
        # if self.dataStart > len(dataLines):
        #     self.dataStart = 0
        # dataLines = dataLines[self.dataStart:]
        data = []
        for dataLine in dataLines:
            if dataLine[0] == "[":
                dataLine = dataLine[1:]
            if dataLine[len(dataLine)-2] == "]":
                dataLine = dataLine[:len(dataLine)-2]
            if "RANGE_INFO" in dataLine:
                try:
                    data.append(json.loads(dataLine))
                except:
                    data.append(json.loads(dataLine[:len(dataLine)-2]))
        logfile.close()
        self.processData(data)

    def processData(self, data):
        self.plotX = []
        self.plotY = []
        exampleId = 0
        if len(data) < self.dataStop:
            self.dataStop = len(data)
        self.dataSets = []
        for k in range(len(self.dropMenuOptions)):
            self.dataSets.append([])
        for k in range(self.dataStop):
            if "RANGE_INFO" in data[k]:
                exampleId = k
                self.dataSets[0].append(data[k]['RANGE_INFO']['precisionRangeM'])
                self.dataSets[1].append(data[k]['RANGE_INFO']['filteredRangeM'])
                self.dataSets[2].append(data[k]['RANGE_INFO']['responderFpp'])
                self.dataSets[3].append(data[k]['RANGE_INFO']['firstPathPower'])
                self.dataSets[4].append(data[k]['RANGE_INFO']['rxPower'])
                self.dataSets[5].append(data[k]['RANGE_INFO']['maxNoise'])
                self.dataSets[6].append(data[k]['RANGE_INFO']['stdNoise'])
                self.dataSets[7].append(data[k]['RANGE_INFO']['firstPathAmp1'])
                self.dataSets[8].append(data[k]['RANGE_INFO']['firstPathAmp2'])
                self.dataSets[9].append(data[k]['RANGE_INFO']['firstPathAmp3'])
                self.dataSets[10].append(data[k]['RANGE_INFO']['maxGrowthCIR'])
                self.dataSets[11].append(data[k]['RANGE_INFO']['rxPreamCount'])
                self.dataSets[12].append(data[k]['RANGE_INFO']['firstPath'])
                self.plotX.append(k)
                self.plotY = self.dataSets[0]
                # self.plotY.append(data[k]['RANGE_INFO']['msgId'])
            self.rangeData.setData(self.plotX, self.plotY)
        self.dataWindow.enableAutoRange(axis = 'y', enable = True)
        self.dataWindow.enableAutoRange(axis = 'x', enable = True)
        self.dataWindow2.enableAutoRange(axis = 'y', enable = True)
        self.dataWindow2.enableAutoRange(axis = 'x', enable = True)
        self.dropMenuChart.setCurrentIndex(1)
        self.updateDropMenuChart()
        # print("\nExample JSON message:\n", data[exampleId])
        print()
        print("Displaying File:", self.filename[0])
        print("Records in logfile:", len(data))
        print(f"Displaying {self.dataStop - self.dataStart} of them")

    def closeItDown(self):
        print("\nLater!\n")

    def updateDropMenuChart(self):
        index = self.dropMenuChart.currentIndex()
        dataY = self.dataSets[index]
        self.plotData.setData(self.plotX, dataY)

    def updateDataLen(self):
        self.dataStart = int(self.dispDataLenStart.text())
        self.dataStop = int(self.dispDataLenStop.text())
        self.readFileData()

    def getLogFilename(self):
        logName = ""
        if self.logPath.is_dir() == True:
            self.filename = QFileDialog.getOpenFileName(self, 'Choose Logfile Name', self.logDir, "log (*.log, *.json)")
        else:
            self.filename = QFileDialog.getOpenFileName(self, 'Choose Logfile Name', "./", "log (*.log, *.json)")
        self.readFileData()

    def initGUI(self):
        # Range Chart
        self.guiFont = guiFonts()
        rPen = pg.mkPen(width = 4, color=(255,0,0))
        bPen = pg.mkPen(width = 4, color=(0,0,255))
        self.dataWindow = pg.PlotWidget(self)
        self.dataWindow.setBackground('w')
        self.dataWindow.setGeometry(5,5,self.graphSizeX-5,int(self.graphSizeY/2)-5)
        self.dataWindow.showGrid(x=True, y=True)
        self.plotX = []
        self.plotY = []
        self.rangeData = self.dataWindow.plot(self.plotX, self.plotY, pen=rPen)

        self.dataWindow2 = pg.PlotWidget(self)
        self.dataWindow2.setBackground('w')
        self.dataWindow2.setGeometry(5,int(self.graphSizeY/2) + 5,self.graphSizeX-5,int(self.graphSizeY/2)-5)
        self.dataWindow2.showGrid(x=True, y=True)
        self.plotX = []
        self.plotY = []
        self.plotData = self.dataWindow2.plot(self.plotX, self.plotY, pen=bPen)

        yStart = 1000
        yBias = 40

        # dropMenuOptions = ["Ranges", "Filtered", "Fpp", "RxPower", "MaxNoise", "StdNoise", "Multi", "MultiFilt"]
        self.dropMenuOptions = ["precisionRangeM", "filteredRangeM", "responderFpp", "firstPathPower", "rxPower", "maxNoise", "stdNoise", "firstPathAmp1", "firstPathAmp2", "firstPathAmp3", "maxGrowthCIR", "rxPreamCount", "firstPath"]
        self.labelDropMenuChart = QLabel(self)
        self.labelDropMenuChart.resize(250, 40)
        self.labelDropMenuChart.move(10, yStart)
        self.labelDropMenuChart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelDropMenuChart.setFont(self.guiFont.guiFont20)
        self.labelDropMenuChart.setText("Chart Options")
        # xWidth = 160
        self.dropMenuChart = QComboBox(self)
        self.dropMenuChart.resize(250,40)
        self.dropMenuChart.move(10,yStart + yBias)
        self.dropMenuChart.setFont(self.guiFont.guiFont20)
        self.dropMenuChart.addItems(self.dropMenuOptions)
        self.dropMenuChart.setEditable(False)
        # self.dropMenuChart.setStyleSheet(self.dropSheetBlue)
        self.dropMenuChart.setToolTip("Pick what should be charted")
        self.dropMenuChart.currentTextChanged.connect(self.updateDropMenuChart)

        self.labelDataLenStart = QLabel(self)
        self.labelDataLenStart.resize(120, 40)
        self.labelDataLenStart.move(300,yStart)
        self.labelDataLenStart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelDataLenStart.setFont(self.guiFont.guiFont18)
        self.labelDataLenStart.setText("Data Start")
        self.dispDataLenStart = QLineEdit(self)
        self.dispDataLenStart.setFont(self.guiFont.guiFont18)
        self.dispDataLenStart.move(300,yStart + yBias)
        self.dispDataLenStart.resize(120,40)
        self.dispDataLenStart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispDataLenStart.setText("4")
        self.dispDataLenStart.editingFinished.connect(self.updateDataLen)

        self.labelDataLenStop = QLabel(self)
        self.labelDataLenStop.resize(120,40)
        self.labelDataLenStop.move(440,yStart)
        self.labelDataLenStop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelDataLenStop.setFont(self.guiFont.guiFont18)
        self.labelDataLenStop.setText("Data Stop")
        self.dispDataLenStop = QLineEdit(self)
        self.dispDataLenStop.setFont(self.guiFont.guiFont18)
        self.dispDataLenStop.move(440,yStart + yBias)
        self.dispDataLenStop.resize(120,40)
        self.dispDataLenStop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispDataLenStop.setText("5000")
        self.dispDataLenStop.editingFinished.connect(self.updateDataLen)

        self.labelDataTotal = QLabel(self)
        self.labelDataTotal.resize(120,40)
        self.labelDataTotal.move(580,yStart)
        self.labelDataTotal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelDataTotal.setFont(self.guiFont.guiFont18)
        self.labelDataTotal.setText("Data Stop")
        self.dispDataTotal = QLineEdit(self)
        self.dispDataTotal.setFont(self.guiFont.guiFont18)
        self.dispDataTotal.move(580,yStart + yBias)
        self.dispDataTotal.resize(120,40)
        self.dispDataTotal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dispDataTotal.setText("-")

        self.but_LogFile = QPushButton('Load LogFile', self)
        self.but_LogFile.setToolTip('Pick LogFile Name')
        self.but_LogFile.resize(200, 40)
        # self.but_LogFile.setStyleSheet(self.gui.buttonSheetBlue)
        self.but_LogFile.setFont(self.guiFont.guiFont14)
        self.but_LogFile.move(720, yStart + yBias)
        self.but_LogFile.clicked.connect(self.getLogFilename)


class guiFonts():
    def __init__(self):
        self.guiFont14 = QFont()
        self.guiFont14.setPixelSize(18)
        self.guiFont18 = QFont()
        self.guiFont18.setPixelSize(22)
        self.guiFont20 = QFont()
        self.guiFont20.setPixelSize(24)
        self.guiFont24 = QFont()
        self.guiFont24.setPixelSize(30)
        self.guiFont30 = QFont()
        self.guiFont30.setPixelSize(38)
        self.guiFont34 = QFont()
        self.guiFont34.setPixelSize(40)
        self.guiFont50 = QFont()
        self.guiFont50.setPixelSize(60)
        self.guiFont100 = QFont()
        self.guiFont100.setPixelSize(120)
        self.guiFont200 = QFont()
        self.guiFont200.setPixelSize(240)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
