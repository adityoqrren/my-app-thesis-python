import numpy as np

class KNNLib:

    def __init__(self, k) -> None:
        self.__k = k

    def fit(self, X_train_tfidf, y_train_tfidf):
        self.X_train_tfidf_list = X_train_tfidf.toarray()
        self.y_train_tfidf_list = y_train_tfidf
    
    def predict(self,X_test_tfidf):
        X_test_list = X_test_tfidf.toarray()
        data_result = np.zeros((len(X_test_list),len(self.X_train_tfidf_list)))
        #print("sebelum: \n",data_result)
        for idx in range (len(X_test_list)):
            # print(idx," - ",X_test[idx])
            # operasi pengurangan data testing dengan all data training
            hasil_pengurangan = np.square(X_test_list[idx] - self.X_train_tfidf_list)
            #print(hasil_pengurangan)

            # menjumlahkan per baris hasil pengurangan
            hasil_sum = np.sum(hasil_pengurangan, axis=1)
            #print(hasil_sum)

            # mengakarkan untuk mencari euclideannya
            hasil_euclidean = np.sqrt(hasil_sum)
            #print(hasil_euclidean)
            data_result[idx] = hasil_euclidean
            #print(hasil_euclidean.shape)
        #print("setelah: \n",data_result)
        
        # mendapatkan index berdasarkan pengurutan data_result (euclidean) jarak terdekat
        order_index_sorted = np.argsort(data_result, 1)
        # mendapatkan label berdasarkan urutan data terdekat
        label_index_sorted = np.take(self.y_train_tfidf_list, order_index_sorted)
        # ambil sebanyak k
        take_k = label_index_sorted[:,:self.__k]
        # menghitung per kelas (voting) kemudian diurutkan dari yang terbesar dan diambil key atau label yang pertama yaitu yang terbesar
        listHasilKlasifikasi = []
        for i in take_k:
            #print(i)
            count_occurences = dict((zip(*np.unique(i, return_counts=True))))
            sorted_dict = dict(sorted(count_occurences.items(), key=lambda item: item[1], reverse=True))
            listHasilKlasifikasi.append(list(sorted_dict.keys())[0])
        return listHasilKlasifikasi #ini returnnya list hasil label setiap data testing
    
    # method yang sama dengan predict tetapi mengembalikan hasil voting
    def predict_vote(self,X_test_tfidf):
        X_test_list = X_test_tfidf.toarray()
        data_result = np.zeros((len(X_test_list),len(self.X_train_tfidf_list)))
        #print("sebelum: \n",data_result)
        for idx in range (len(X_test_list)):
            # print(idx," - ",X_test[idx])
            hasil_pengurangan = np.square(X_test_list[idx] - self.X_train_tfidf_list)
            #print(hasil_pengurangan)
            hasil_sum = np.sum(hasil_pengurangan, axis=1)
            #print(hasil_sum)
            hasil_euclidean = np.sqrt(hasil_sum)
            #print(hasil_euclidean)
            data_result[idx] = hasil_euclidean
            #print(hasil_euclidean.shape)
        #print("setelah: \n",data_result)
        order_index_sorted = np.argsort(data_result, 1)
        label_index_sorted = np.take(self.y_train_tfidf_list, order_index_sorted)
        take_k = label_index_sorted[:,:self.__k]
        all_dict_label = []
        for i in take_k:
            #print(i)
            count_occurences = dict((zip(*np.unique(i, return_counts=True))))
            sorted_dict = dict(sorted(count_occurences.items(), key=lambda item: item[1], reverse=True))
            all_dict_label.append(sorted_dict)
        return all_dict_label #ini returnnya vote masing2 kelas