import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# from homepage_control import HomePageControl
from Ui_WaitingDialog import Ui_WaitingDialog
from PyQt5.QtCore import QTimer

class WaitingDialogControl(QtWidgets.QDialog, Ui_WaitingDialog):

    def __init__(self, parent=None):
        super(WaitingDialogControl, self).__init__(parent)
        self.setupUi(self)
        #timer = QTimer()
        self.startAnimation()
        #timer.singleShot(3000, self.stopAnimation)
        #self.indicator_open = 0
        #self.btn_stop.clicked.connect(self.onStopProgress)

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()

    # def changeIndicatorOpen(self):
    #     self.indicator_open = 1
    
    # def onStopProgress(self):
    #     self.close()
    #     print("button stop diklik")
    #     self.indicator_open = 0
