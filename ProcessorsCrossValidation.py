from PyQt5.QtCore import (
    QThread, pyqtSignal
)
from InformationGainProcess import InformationGainProcess
from MKNNLib import MKNNLib
from KNNLib import KNNLib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# import time
#import logging

#logging.basicConfig(format="%(message)s", level=logging.INFO)

class ProcessorsCrossValidation(QThread):

    finished = pyqtSignal(list)

    def setMyData(self, myData, myIndexTrainingList, myIndexTestingList, k, igTreshold, indicatorClassifier, indicatorThread):
        #print("data di processors cross validation: ", myData.shape)
        self.__myData = myData
        self.__myIndexTrainingList = myIndexTrainingList
        self.__myIndexTestingList = myIndexTestingList
        self.__k = k
        self.__igTreshold = igTreshold
        self.__indicatorClassifier = indicatorClassifier
        self.__indicatorThread = indicatorThread
        print("self.__indicatorThread: ", self.__indicatorThread)

    def __splitting(self, indexTraining, indexTesting):
        X_train = self.__myData['tweet_stemming'].loc[indexTraining]
        X_test = self.__myData['tweet_stemming'].loc[indexTesting]
        y_train = list(self.__myData['Label'].loc[indexTraining])
        y_test= list(self.__myData['Label'].loc[indexTesting])

        return X_train, X_test, y_train, y_test
        
    # method menghitung information gain
    def __countInformationGain(self, X_train, y_train):
        #print("Masuk ke IG")
        igProcess = InformationGainProcess(X_train, y_train)
        IGvocabulary = igProcess.IG_process(self.__igTreshold)
        return IGvocabulary

    #inisialisasi count vectorizer : term frquency
    def __do_nothing(self, tokens):
        return tokens

    def __pembobotan(self, IGvocabulary, X_train, X_test):
        #count data training

        if(len(IGvocabulary)==0):
            # jika tidak melakukan seleksi fitur maka menggunakan fitur dari data 
            count_vect = CountVectorizer(
                tokenizer = self.__do_nothing,
                preprocessor = None,
                lowercase = False,
            )
        else:
            # jika melakukan seleksi fitur makan menggunakan fitur yang didapatkan dari hasil seleksi (IGVocabulary)
            count_vect = CountVectorizer(
                tokenizer = self.__do_nothing,
                preprocessor = None,
                lowercase = False,
                vocabulary = IGvocabulary
            )

        # fit dan transform ke count_vect
        X_train_counts = count_vect.fit_transform(X_train)

        #tfidf data training
        tfidf_transformer =  TfidfTransformer(smooth_idf=False, use_idf=True, norm=None)
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        #count data testing
        X_test_count = count_vect.transform(X_test)

        #tfidf data testing
        X_test_tfidf = tfidf_transformer.transform(X_test_count)

        return X_train_tfidf, X_test_tfidf

    def __prosesKNN(self, X_train_tfidf, y_train, X_test_tfidf):
        #print("Masuk ke KNN")
        knnLib = KNNLib(self.__k)
        knnLib.fit(X_train_tfidf, y_train)
        label_predicted = knnLib.predict(X_test_tfidf)
        return label_predicted

    def __prosesMKNN(self, X_train_tfidf, y_train, X_test_tfidf):
        #print("Masuk ke MKNN")
        mknnLib = MKNNLib(self.__k)
        mknnLib.fit(X_train_tfidf, y_train)
        label_predicted = mknnLib.predict(X_test_tfidf)
        return label_predicted

    def run(self):
        listAllResult = []
        for y in range(len(self.__myIndexTrainingList)):
            #finish preprocessing, start splitting
            X_train, X_test, y_train, y_test = self.__splitting(self.__myIndexTrainingList[y], self.__myIndexTestingList[y])
            #finish splitting, start information gain
            if(self.__igTreshold>0):
                IGVocabulary = self.__countInformationGain(X_train, y_train)
                print("term IG teratas: ",IGVocabulary[:10])
                print("term IG terbawah: ",IGVocabulary[-10:])
                #finish information gain, start pembobotan
            else:
                IGVocabulary = []
                #logging.info(f"No IG, start pembobotan")
                #finish splitting, start pembobotan
            X_train_tfidf, X_test_tfidf = self.__pembobotan(IGVocabulary, X_train, X_test)
            #finish pembobotan, start classification
            if(self.__indicatorClassifier==0):
                label_predicted = self.__prosesKNN(X_train_tfidf, y_train, X_test_tfidf)
            else:
                label_predicted = self.__prosesMKNN(X_train_tfidf, y_train, X_test_tfidf)
            listAllResult.append((self.__myIndexTrainingList[y], self.__myIndexTestingList[y], y_test, label_predicted))
        self.finished.emit(listAllResult)