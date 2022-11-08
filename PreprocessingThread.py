from PyQt5.QtCore import (
    QThread, pyqtSignal
)
from Preprocessing import Preprocessing

class PreprocessingThread(QThread):
    resultProcessed = pyqtSignal(object)
    finished = pyqtSignal()

    def setMyData(self, myData):
        self.__myData = myData

    def run(self):
        # panggil library Preprocessing
        print("Masuk ke preprocessing")
        preprocessing = Preprocessing()
        hasil_preprocessing = preprocessing.processData(self.__myData)
        self.resultProcessed.emit(hasil_preprocessing)
        self.finished.emit()