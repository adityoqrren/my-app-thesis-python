
# Press the green button in the gutter to run the script.
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
#from welcomepage import Ui_WelcomePage
#import welcomepage_control
from WelcomePageControl import WelcomePageControl

def run():
    app = QtWidgets.QApplication(sys.argv)
    ui = WelcomePageControl()
    ui.homepageControl.actionKembali.triggered.connect(
        lambda:changeWindow(ui,ui.homepageControl)
    )
    ui.homepageControl.actionExit.triggered.connect(
        ui.homepageControl.close
    )
    ui.show()
    return app.exec_()

def changeWindow(w1, w2):
    w2.hide()
    w1.show()

if __name__ == '__main__':
    import sys
    sys.exit(run())
