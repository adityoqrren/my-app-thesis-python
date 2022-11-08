import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import (
    QMutex, Qt, QObject, QThread, pyqtSignal
)

class Worker(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(tuple)

    def setMyData(self, myData):
        self.__myData = myData
        self.__numRows = myData.shape[0]
        self.__numColumns = myData.shape[1]

    def run(self):
        """Long-running task"""
        for i in range(self.__numRows):
            for j in range(self.__numColumns):
                self.progress.emit((i,j,str(self.__myData.iloc[i,j])))
        self.finished.emit()