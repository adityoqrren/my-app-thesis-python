# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waiting_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer

class Ui_WaitingDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(288, 207)
        Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.btn_stop = QtWidgets.QPushButton(Dialog)
        self.btn_stop.setGeometry(QtCore.QRect(200, 150, 75, 23))
        self.btn_stop.setObjectName("btn_stop")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(100, 30, 87, 71))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        #QLabel for indicator
        self.loading_indicator = QtWidgets.QLabel(self.widget)
        self.loading_indicator.setAlignment(QtCore.Qt.AlignCenter)
        #QMovie
        self.movie = QMovie('loading_gif.gif')
        self.loading_indicator.setMovie(self.movie)
        self.verticalLayout.addWidget(self.loading_indicator)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_stop.setText(_translate("Dialog", "Stop"))
        self.label.setText(_translate("Dialog", "Mohon Tunggu"))
        self.label_2.setText(_translate("Dialog", "Sedang diproses"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_WaitingDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
