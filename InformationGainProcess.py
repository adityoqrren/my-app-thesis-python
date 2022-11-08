import pandas as pd
import numpy as np
from InformationGainLib import InformationGainLib
from sklearn.feature_extraction.text import CountVectorizer

class InformationGainProcess:

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __do_nothing(self, tokens):
        return tokens

    def IG_process(self, treshold):
        #sebelum kita melakukan information gain kita harus menghitung kemunculan dan ketidakmunculan term dalam dokumen tapi dengan binaryu saja bukan dihitung frekuensinya
        #inisialisasi count vectorizer : term frquency
        count_vect_binary = CountVectorizer(
                tokenizer = self.__do_nothing,
                preprocessor = None,
                lowercase = False,
                binary = True
        )

        X_train_counts_binary = count_vect_binary.fit_transform(self.X)
        #ubah ke numpy array dan transpose
        X_train_counts_dense = X_train_counts_binary.toarray()
        X_train_counts_trans = X_train_counts_dense.T
        #hitung semua IG per kata
        iglib = InformationGainLib()
        hasilIG = iglib.countInformationGain(X_train_counts_trans, self.y)
        # jadiin dataframe biar bisa dimanipulasi
        df_kata_ig = pd.DataFrame(hasilIG)
        # mengambil fitur kata dari count_vect
        df_kata_ig['kata'] = count_vect_binary.get_feature_names()
        # print("count features: ", len(df_kata_ig['kata']))
        #sorting dataframe ig
        df_kata_ig_sorted = df_kata_ig.sort_values(0,ascending=False)
        #pilih berdasarkan treshold (percent) 
        jumlah_kata_diambil = round(df_kata_ig_sorted.shape[0] * (treshold/100))
        df_treshold_percent = df_kata_ig_sorted.iloc[0:jumlah_kata_diambil]
        # print("count features after IG: ", len(df_treshold_percent))
        return list(df_treshold_percent['kata'])