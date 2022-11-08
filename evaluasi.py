from sklearn.metrics import confusion_matrix

class Evaluasi():

    @staticmethod
    def getConfusionMatrix(y_actual, y_pred):
        return confusion_matrix(y_actual, y_pred, labels=[0,1]).ravel()

    @staticmethod
    def countAccuracy(tn,fp,fn,tp):
        myAcc = (tp+tn)/(tp+fp+fn+tn)
        return myAcc

    @staticmethod
    def countPrecision(tp,fp):
        if tp == 0 and fp == 0:
            myPrec = 0
        else:
            myPrec =  tp/(tp+fp)
        return myPrec

    @staticmethod
    def countRecall(tp,fn):
        if tp==0 and fn==0:
            myRecall = 0
        else:
            myRecall = tp/(tp+fn)
        return myRecall

    @staticmethod
    def countF1(precision, recall):
        if recall == 0 and precision == 0 :
            myF1 = 0
        else:
            myF1 = 2 * (recall * precision)/(recall + precision)
        return myF1
