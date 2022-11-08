import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import (
    QMutex, QObject, QThread, pyqtSignal
)
from Ui_HomePage import Ui_HomePage
from PreprocessingThread import PreprocessingThread
from WaitingDialogControl import WaitingDialogControl
from sklearn.model_selection import StratifiedKFold
from ProcessorsCrossValidation import ProcessorsCrossValidation
from HasilEvaluasiControl import HasilEvaluasiControl

import pandas as pd
import time

from WarningDialogControl import WarningDialogControl

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


class HomePageControl(QtWidgets.QMainWindow, Ui_HomePage):

    def __init__(self, parent=None):
        super(HomePageControl, self).__init__(parent)
        self.setupUi(self)
        # jika button "KNN" atau "KNN dan IG" diklik
        self.btn_algo_knn.clicked.connect(lambda: self.__onTestDialogKNN_MKNN(0))
        self.btn_algo_knn_ig.clicked.connect(lambda: self.__onTestDialogKNN_MKNN_IG(0))
        self.btn_algo_mknn.clicked.connect( lambda: self.__onTestDialogKNN_MKNN(1))
        self.btn_algo_mknn_ig.clicked.connect(lambda: self.__onTestDialogKNN_MKNN_IG(1))
        self.btn_cv_splitting.clicked.connect(self.__onRunSplitting)
        self.btn_cv_deletesplit.clicked.connect(self.__onRunDeleteSplit)

        # pembuatan object
        self.hasilEvaluasiCrossValidation = HasilEvaluasiControl()
        self.waitingDialog = WaitingDialogControl()
        self.warningDialog = WarningDialogControl()
        self.__resultCrossValidation = []
        self.mutex = QMutex()
        self.__train_index_list = []
        self.__test_index_list = []

    def setPathFileDipilih(self, path):
        self.__pathFileDipilih = path
        self.__myData = pd.read_csv(self.__pathFileDipilih)

    def __setTableData(self, dataTuple):
        self.tabel_data.setItem(dataTuple[0],dataTuple[1],QTableWidgetItem(str(dataTuple[2])))

    def showFileDipilih(self):
        numRows = self.__myData.shape[0]
        numColumn = self.__myData.shape[1]
        self.label_file_data.setText(os.path.basename(self.__pathFileDipilih))
        self.label_baris_data.setText(str(numRows))
        self.label_kolom_data.setText(str(numColumn))
        label_value_counts = self.__myData['Label'].value_counts()
        self.label_jumlah_positif.setText(str(label_value_counts[1]))
        self.label_jumlah_negatif.setText(str(label_value_counts[0]))
        self.tabel_data.setColumnCount(numColumn)
        self.tabel_data.setRowCount(numRows)
        self.tabel_data.setHorizontalHeaderLabels(self.__myData.columns)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.setMyData(self.__myData)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.__setTableData)
        self.thread.start()


    def __finishTaskCrossValidation(self, myList):
        #mungkin saat thread A excute code ini thread B udah execute writeResultCrossValidation jadi listnya udah bertambah
        # solusi : writeResultCrossValidation dan finishTaskCrossValidation disatuin
        self.mutex.lock()
        self.__resultCrossValidation.extend(myList)
        # print("finishedTask: ", len(myList))
        self.mutex.unlock()
        if(len(self.__resultCrossValidation)==10):
            '''panggil window hasil_evaluasi_cross_validation -> kita harus pake self biar nggak dihancurkan
            saat thread ini difinish. Jadi object ini punya homepage_control'''
            self.time_end = time.time()
            print(str(round(self.time_end-self.time_start,5)))
            self.hasilEvaluasiCrossValidation.show()
            self.hasilEvaluasiCrossValidation.setDataResume(self.__resultCrossValidation, self.select_k_value.value(), self.igSelected, self.classifierSelected)

            self.__resultCrossValidation = []
            self.waitingDialog.hide()

    
    # splitting data based on index
    def __onRunSplitting(self):
        # membagi index jadi 10 bagian
        self.__cv = StratifiedKFold(n_splits=10, shuffle=True)
        count = 0
        for train_index, test_index in self.__cv.split(self.__myData, self.__myData['Label']):
            count = count+1
            self.__train_index_list.append(train_index)
            self.__test_index_list.append(test_index)
        if len(self.__train_index_list) == 10 and len(self.__test_index_list) == 10:
            print("train: ",self.__train_index_list)
            print("test: ",self.__test_index_list)
            self.split_indicator.setText('Index data sudah displit')

    def __onRunDeleteSplit(self):
        self.__train_index_list.clear()
        self.__test_index_list.clear()
        if len(self.__train_index_list)==0 and len(self.__train_index_list)==0:
            self.split_indicator.setText('Belum dilakukan splitting')

    def __runCrossValidation(self, myDataProcessed):

        mid = int(len(self.__train_index_list)/2)

        #Worker 1 (Thread 1) pemrosesan cross validation
        self.workerProcess = ProcessorsCrossValidation()
        self.workerProcess.setMyData(myDataProcessed, self.__train_index_list[:mid], self.__test_index_list[:mid], self.select_k_value.value(), self.igSelected, self.classifierSelected, 1)
        self.workerProcess.finished.connect(
            self.__finishTaskCrossValidation
        )
        self.workerProcess.finished.connect(self.workerProcess.deleteLater)
        self.workerProcess.start()


        # Worker 2 (Thread 2) pemrosesan cross validation
        self.workerProcess2 = ProcessorsCrossValidation()
        self.workerProcess2.setMyData(myDataProcessed, self.__train_index_list[mid:], self.__test_index_list[mid:],self.select_k_value.value(), self.igSelected, self.classifierSelected, 2)
        self.workerProcess2.finished.connect(
            self.__finishTaskCrossValidation
        )
        self.workerProcess2.finished.connect(self.workerProcess2.deleteLater)
        self.workerProcess2.start()


    def __onTestDialogKNN_MKNN(self, classifierSelected):
        if(self.__train_index_list and self.__test_index_list):
            if(self.btn_training_testing.isChecked() is True
                    and self.select_k_value.value()>0):

                self.igSelected = 0
                self.classifierSelected = classifierSelected

                self.time_start = time.time()
                # masuk ke preprocessing dahulu
                self.workerPreprocessing = PreprocessingThread()
                self.workerPreprocessing.setMyData(self.__myData)
                self.workerPreprocessing.finished.connect(self.workerPreprocessing.deleteLater)
                self.workerPreprocessing.finished.connect(self.workerPreprocessing.quit)
                self.workerPreprocessing.resultProcessed.connect(self.__runCrossValidation)
                self.workerPreprocessing.start()
                self.waitingDialog.btn_stop.clicked.connect(
                    lambda: self.__threadKill()
                )
                self.waitingDialog.show()
            else:
                print(self.select_k_value.value())
                self.warningDialog.setMessage("Isi value k terlebih dahulu")
                self.warningDialog.show()
        else:
            self.warningDialog.setMessage("Split data terlebih dahulu")
            self.warningDialog.show()
    
    def __threadKill(self):
        try:
            self.workerPreprocessing.terminate()
        except:
            print("workerPreprocessing has been deleted")
            self.workerProcess.terminate()
            self.workerProcess2.terminate()
        self.waitingDialog.hide()

    def __onTestDialogKNN_MKNN_IG(self, classifierSelected):
        if(self.__train_index_list and self.__test_index_list):
            if(self.btn_training_testing.isChecked() is True
                    and self.select_k_value.value()>0):

                self.igSelected = self.select_ig_value.value()
                self.classifierSelected = classifierSelected

                if(self.select_ig_value.value() > 0):
                    self.time_start = time.time()
                    # masuk ke preprocessing dahulu
                    self.workerPreprocessing = PreprocessingThread()
                    self.workerPreprocessing.setMyData(self.__myData)
                    self.workerPreprocessing.finished.connect(self.workerPreprocessing.deleteLater)
                    self.workerPreprocessing.resultProcessed.connect(self.__runCrossValidation)
                    self.workerPreprocessing.start()
                    self.waitingDialog.btn_stop.clicked.connect(
                        lambda: self.__threadKill()
                    )
                    self.waitingDialog.show()
                else:
                    self.warningDialog.setMessage("Isi value treshold terlebih dahulu")
                    self.warningDialog.show()
            else:
                print(self.select_k_value.value())
                self.warningDialog.setMessage("Isi value k terlebih dahulu")
                self.warningDialog.show()
        else:
                self.warningDialog.setMessage("Split data terlebih dahulu")
                self.warningDialog.show()

