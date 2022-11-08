import math
import numpy as np

class InformationGainLib:

    # allData berbentuk matrix numpy berasal dari proses count vectorizer binary yang telah ditranspose dan diubah menjadi list
    def countInformationGain(self, allData, allDataLabel):
        allScore = []
        # print("allData: ", allData)
        for x in allData:
            # print("x: ", x)
            allScore.append(self.__InformationGain(x, allDataLabel))
        return allScore
    #keluaran berupa list score semua nilai

    def __InformationGain(self, data, dataLabel):
        n = len(data)
        #hitung kemunculan setiap label
        label, y = np.unique(dataLabel, return_counts=True)
        # menghitung fitur pada setiap label
        y0, y1 = self.__countKemunculan(data, dataLabel)
        #entropy kemunculan
        entropyKemunculan = self.__Entropy(y1)
        #entropy ketidakmunculan 
        entropyKetidakmunculan = self.__Entropy(y0)
        #entropy semua
        entropySemua = self.__Entropy(y)
        IG = self.__countGain(y0,y1,n,entropySemua, [entropyKetidakmunculan,entropyKemunculan])
        return IG

    #fungsi untuk mencari kemunculan
    def __countKemunculan(self, studyCaseX, studyCaseY):
        countLabel=len(set(studyCaseY))
        #print(countLabel)
        dictNested_y1 =  np.zeros(countLabel)#muncul
        dictNested_y0 =  np.zeros(countLabel)#tidak muncul
        # print("studyCaseX: ", studyCaseX)
        for i in range(len(studyCaseX)):
            if studyCaseX[i] == 1:
                dictNested_y1[studyCaseY[i]] = dictNested_y1[studyCaseY[i]] + 1
            else:
                dictNested_y0[studyCaseY[i]] = dictNested_y0[studyCaseY[i]] + 1

        return dictNested_y0, dictNested_y1

    #fungsi untuk mencari entropy 
    # return 0 jika terdapat 0 pada salah satu kelas karena jika dihitung ujung2nya 0 juga. Sedangkan kelas yg beneran 0 kita 0-kan karena tidak bisa dihitung
    def __Entropy(self, y):
        n = sum(y)
        if 0 not in y:
            H_inside = (y/n)*np.log2(y/n)
            H_result = sum(H_inside)
            return H_result * -1
        else:
            return 0

    def __HSx(self, n,list_n_y, H_Sy):
        #print(list_n_y)
        HSx_result = 0
        for i in range(len(H_Sy)):
            HSx_result += (list_n_y[i]/n)*H_Sy[i]
            #print(HSx_result)
        return HSx_result

    def __countGain(self, y0,y1,n,HS,H_Sy):
        n_y0 = sum(y0)
        n_y1 = sum(y1)
        list_n_y = [n_y0, n_y1]
        IGx = HS - self.__HSx(n,list_n_y, H_Sy)
        return IGx