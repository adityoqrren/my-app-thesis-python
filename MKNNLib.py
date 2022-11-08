import math
import numpy as np

class MKNNLib:

    def __init__(self, k) -> None:
        self.__k = k
    
    # fungsi euclidean
    def euclidean_np(self, X_test, X_train):
        data_result = np.zeros((len(X_test),len(X_train)))
        for idx in range (len(X_test)):
            hasil_pengurangan = np.square(X_test[idx] - X_train)
            hasil_sum = np.sum(hasil_pengurangan, axis=1)
            hasil_euclidean = np.sqrt(hasil_sum)
            data_result[idx] = hasil_euclidean
        return data_result 

    #fungsi sorting
    def sorting_np(self, arr_np):
        # sorting dan return indexnya
        my_arr_indexsort = np.argsort(arr_np, axis=1)
        # ngambil nilai array berdasarkan index yang telah disorting
        my_arr_sorted = np.take_along_axis(arr_np, my_arr_indexsort, axis=1)
        return my_arr_sorted, my_arr_indexsort
    
    #fungsi untuk menghitung validity setiap data training
    def countAllValidity_np(self, jarak_training_params, label_data_training, h):
        validity_training = []
        # sorting hasil perhitungan jarak setiap data training ke data training lainnya dan ambil label data dari label J label training terdekat
        arr_sorting, arr_sorting_index = self.sorting_np(jarak_training_params)
        sorted_label_arr = np.take(label_data_training, arr_sorting_index)
        #buang data pertama karena itu data sekarang, ambil data dari data kedua (index 1) sampai data ke h
        for_validity_label = sorted_label_arr[:,1:(h+1)] #All label sorted distance selected
        #hitung yang labelnya sama dengan data sekarang
        for idx, arr_now in enumerate(for_validity_label):
            sum_same_label = len(arr_now[arr_now==label_data_training[idx]])
            validity = (1/h) * sum_same_label 
            validity_training.append(validity)
        return validity_training
    
    #fungsi untuk menghitung weight
    def weight_np(self, data_testing, data_training, label_training, k,validity_training_arr):
        #kita hitung jarak antara data testing ke semua data training
        euclidean_testing_training = self.euclidean_np(data_testing,data_training)
        #kita sorting dari terkecil sampai terbesar
        arr_sorting, arr_sorting_index = self.sorting_np(euclidean_testing_training)
        sorted_validity_arr = np.take(validity_training_arr, arr_sorting_index)
        #print("sorted validity arr: ", sorted_validity_arr)
        sorted_label_arr = np.take(label_training, arr_sorting_index)
        #potong jadi sebanyak k
        selected_distance = arr_sorting[:,:k] #All sorted distance selected
        selected_distance_validity = sorted_validity_arr[:,:k] #All validity sorted distance selected
        selected_distance_label = sorted_label_arr[:,:k] #All label sorted distance selected
        #mulai penghitungan bobot untuk masing2 data training terdekat dengan data testing
        all_weight = selected_distance_validity * (1/(selected_distance + 0.5))
        return all_weight, selected_distance_label

    #count weight by class
    def countWeightByClass_np(self, weightJarak, labelJarak):
        # print("weightJarak: ",weightJarak.shape)
        # print("labelJarak: ",labelJarak.shape)
        all_dict_label = []
        all_label_test_predicted = []
        for x in range(len(weightJarak)):
            dict_label = {}
            for y in range(len(weightJarak[x])):
                if labelJarak[x,y] in dict_label:
                    dict_label[labelJarak[x,y]] += weightJarak[x,y]
                else:
                    dict_label[labelJarak[x,y]] = weightJarak[x,y]
            sorted_dict = dict(sorted(dict_label.items(), key=lambda item: item[1], reverse=True))
            # print("sorted_dict: ", sorted_dict)
            all_dict_label.append(sorted_dict)
            all_label_test_predicted.append(list(sorted_dict.keys())[0])
            
        return all_dict_label, all_label_test_predicted

    def fit(self, X_train_tfidf, y_train_tfidf):
        self.X_train_tfidf_list = X_train_tfidf.toarray()
        self.y_train_list = y_train_tfidf
    
    def predict(self, X_test_tfidf):
        """
        menerima array testing data
        kita predict dan balikannya adalah kelasnya
        """
        # hitung jarak per data training ke data training lainnya
        jarak_training = self.euclidean_np(self.X_train_tfidf_list, self.X_train_tfidf_list)
        # hitung H
        H = int(0.1 * len(self.X_train_tfidf_list))
        # hitung validitas setiap data training
        allValidity = self.countAllValidity_np(jarak_training, self.y_train_list, H)
        # dapatkan bobot masing-masing k data terdekat
        weight_data_all, selected_label = self.weight_np(X_test_tfidf.toarray(), self.X_train_tfidf_list, self.y_train_list, self.__k,allValidity)
        list_dict_label, listHasilKlasifikasi = self.countWeightByClass_np(weight_data_all, selected_label)
        return listHasilKlasifikasi

    def predict_vote(self, X_test_tfidf):
        """
        menerima array testing data
        kita predict dan balikannya adalah hasil vote setiap kelas
        """
        # hitung jarak per data training ke data training lainnya
        jarak_training = self.euclidean_np(self.X_train_tfidf_list, self.X_train_tfidf_list)
        # hitung H
        H = int(0.1 * len(self.X_train_tfidf_list))
        # hitung validitas setiap data training
        allValidity = self.countAllValidity_np(jarak_training, self.y_train_list, H)
        # dapatkan bobot masing-masing k data terdekat
        weight_data_all, selected_label = self.weight_np(X_test_tfidf.toarray(), self.X_train_tfidf_list, self.y_train_list, self.__k,allValidity)
        list_dict_label, listHasilKlasifikasi = self.countWeightByClass_np(weight_data_all, selected_label)
        return list_dict_label