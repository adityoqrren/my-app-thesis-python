from PyQt5 import QtWidgets
from Ui_WarningDialog import Ui_WarningDialog

class WarningDialogControl(QtWidgets.QDialog, Ui_WarningDialog):

    def __init__(self, parent=None):
        super(WarningDialogControl, self).__init__(parent)
        self.setupUi(self)
    
    def setMessage(self, message):
        self.nama_warning.setText(message)