import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from HomePageControl import HomePageControl
from Ui_WelcomePage import Ui_WelcomePage


class WelcomePageControl(QtWidgets.QMainWindow, Ui_WelcomePage):

    def __init__(self, parent=None):
        super(WelcomePageControl, self).__init__(parent)
        self.setupUi(self)
        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_submit.clicked.connect(self.onSubmit)
        self.homepageControl = HomePageControl()

    def open_file(self):
        self.__path, filetype = QFileDialog.getOpenFileName(self,
                                                        "Select File",
                                                        "./",
                                                        "csv (*.csv)")
        nama_file_dipilih = os.path.basename(self.__path)

        #print("di welcomepage_control: ",self.path)
        if nama_file_dipilih is not '':
            self.label_nama_file.setText(nama_file_dipilih)

    def onSubmit(self):
        #tadi tu karena getPath nya ditaro' di __init__ jadi itu kan pas ngebuat object langsung dieksekusi
        #ya nggak masuk lah. Karena belum kita set. Kita set kan setelah terbentuk objectnya
        self.homepageControl.setPathFileDipilih(self.__path)
        self.homepageControl.show()
        #harusnya kalo ngeprint disini aja jadi masuk dianya
        self.hide()
        self.homepageControl.showFileDipilih()

