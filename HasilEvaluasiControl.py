import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
from collections import Counter
from evaluasi import Evaluasi
#import library untuk analisa

from PyQt5.QtWidgets import (QTableWidgetItem, QFileDialog)

from Ui_HasilEvaluasi import Ui_HasilEvaluasi

class HasilEvaluasiControl(QtWidgets.QMainWindow, Ui_HasilEvaluasi):

    def __init__(self, parent=None):
        super(HasilEvaluasiControl, self).__init__(parent)
        self.setupUi(self)
        self.actionKinerja.triggered.connect(self.__saveKinerja)
        self.actionConfusion.triggered.connect(self.__saveConfusion)
    
    def setDataResume(self, listResume, k, igTreshold, indicatorClassifier):
        self.__listResume = listResume
        allAccuracy = 0
        allRecall = 0
        allPrecision = 0
        allFMeasure = 0

        self.__setNamaAlgoritma(igTreshold, k, indicatorClassifier)

        #set number row and column
        self.tabel_cf.setRowCount(10)
        self.tabel_cf.setColumnCount(7)

        self.tabel_kinerja.setRowCount(10)
        self.tabel_kinerja.setColumnCount(5)

        #inisialisasi list untuk ngesave hasil
        jumlahTestClass_pos_list = []
        jumlahTestClass_neg_list = []
        TP_list = []
        FP_list = []
        FN_list = []
        TN_list = []
        acc_list = []
        rec_list = []
        prec_list = []
        fm_list = []

        for index, dataTuple in enumerate(self.__listResume):
            # indexTraining = dataTuple[0]
            # indexTesting = dataTuple[1]
            y_test = dataTuple[2]
            y_predicted = dataTuple[3]

            tn, fp, fn, tp = Evaluasi.getConfusionMatrix(y_test, y_predicted)

            #masukkan jumlah ke table
            jumlahTestClass = Counter(y_test)
            jumlahTestClass_pos = jumlahTestClass[1]
            jumlahTestClass_neg = jumlahTestClass[0]

            #isi table confusion matrix dan isi list
            self.tabel_cf.setItem(index, 0, QTableWidgetItem(str(index+1)))
            self.tabel_cf.setItem(index, 1, QTableWidgetItem(str(jumlahTestClass_pos)))
            self.tabel_cf.setItem(index, 2, QTableWidgetItem(str(jumlahTestClass_neg)))
            self.tabel_cf.setItem(index, 3, QTableWidgetItem(str(tp)))
            self.tabel_cf.setItem(index, 4, QTableWidgetItem(str(fp)))
            self.tabel_cf.setItem(index, 5, QTableWidgetItem(str(fn)))
            self.tabel_cf.setItem(index, 6, QTableWidgetItem(str(tn)))

            #add ke list
            jumlahTestClass_pos_list.append(jumlahTestClass_pos)
            jumlahTestClass_neg_list.append(jumlahTestClass_neg)
            TP_list.append(tp)
            FP_list.append(fp)
            FN_list.append(fn)
            TN_list.append(tn)

            # accuracy
            myAccuracy = Evaluasi.countAccuracy(tn,fp,fn,tp)
            allAccuracy = allAccuracy + myAccuracy
            # precision
            myPrecision = Evaluasi.countPrecision(tp, fp)
            allPrecision = allPrecision + myPrecision
            # recall
            myRecall = Evaluasi.countRecall(tp, fn)
            allRecall = allRecall + myRecall
            # FMeasure
            myFMeasure = Evaluasi.countF1(myPrecision, myRecall)
            allFMeasure = allFMeasure + myFMeasure

            # isi table kinerja
            self.tabel_kinerja.setItem(index, 0, QTableWidgetItem(str(index+1)))
            self.tabel_kinerja.setItem(index, 1, QTableWidgetItem(str(round(myAccuracy,3))))
            self.tabel_kinerja.setItem(index, 2, QTableWidgetItem(str(round(myRecall,3))))
            self.tabel_kinerja.setItem(index, 3, QTableWidgetItem(str(round(myPrecision,3))))
            self.tabel_kinerja.setItem(index, 4, QTableWidgetItem(str(round(myFMeasure,3))))

            # tambah ke list
            acc_list.append(myAccuracy)
            prec_list.append(myPrecision)
            rec_list.append(myRecall)
            fm_list.append(myFMeasure)
            
        #print("allAccuracy: ", allAccuracy, " \nallRecall: ", allRecallPos, "\nallPrecision: ", allPrecisionPos, "\nallF1: ", allF1Pos)

        ratarataAccuracy = allAccuracy/10
        self.accuracy_rata.setText(str(round(ratarataAccuracy, 3)))

        #isi tabel kinerja rata-rata
        ratarataPrecision = allPrecision/10
        self.precision_rata.setText(str(round(ratarataPrecision, 3)))
        ratarataRecall = allRecall/10
        self.recall_rata.setText(str(round(ratarataRecall, 3)))
        ratarataFMeasure = allFMeasure/10
        self.fmeasure_rata.setText(str(round(ratarataFMeasure, 3)))

        #pembuatan dataframe confusion
        self.__df_confusion = pd.DataFrame({
            'Jumlah Pos':jumlahTestClass_pos_list,
            'Jumlah Neg':jumlahTestClass_neg_list,
            'TP':TP_list,
            'FP':FP_list,
            'FN':FN_list,
            'TN':TN_list})
        self.__df_kinerja = pd.DataFrame({
            'Accuracy':acc_list,
            'Recall':rec_list,
            'Precision':prec_list,
            'F-Measure': fm_list
        })
        self.__df_kinerja.loc['Rata-rata'] = [ratarataAccuracy, ratarataRecall, ratarataPrecision, ratarataFMeasure]
        self.__df_kinerja = self.__df_kinerja.round(3)
    
    def __setNamaAlgoritma(self, igTreshold, k, indicatorClassifier):
        if igTreshold==0 and indicatorClassifier==0:
            self.label_nama_algoritma.setText("Algoritma K-NN (k={})".format(k))
        elif igTreshold==0 and indicatorClassifier==1:
            self.label_nama_algoritma.setText("Algoritma MK-NN (k={})".format(k))
        elif igTreshold>0 and indicatorClassifier== 0:
            self.label_nama_algoritma.setText("Algoritma K-NN (k={}) + IG {}%".format(k, igTreshold))
        else:
            self.label_nama_algoritma.setText("Algoritma MK-NN (k={}) + IG {}%".format(k, igTreshold))
    
    def __saveConfusion(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', "./", "Excel File (*.xlsx)")
        if(name[0]!=''):
            self.__df_confusion.to_excel(name[0])

    def __saveKinerja(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', "./", "Excel File (*.xlsx)")
        if(name[0]!=''):
            self.__df_kinerja.to_excel(name[0])



    
