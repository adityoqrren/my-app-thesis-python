import pandas as pd
import nltk
import string
#from nltk import word_tokenize
import re
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessing:

    def processData(self, data):
        # data dicopy agar tidak mempengaruhi parameter yang dimasukkan
        processData = data.copy()
        #print("data di method processData: ",processData.shape)
        #parameter data adalah data dalam bentuk dataframe
        #casefolding
        data_lower = processData['Text Tweet'].str.lower()
        processData['tweet_lowered'] = data_lower
        #cleaning data
        data_cleaned = self.__cleaningData(processData['tweet_lowered'])
        processData['tweet_cleaned'] = data_cleaned
        #Tokenizing
        data_tokenized = self.__wordTokenizing(processData['tweet_cleaned'])
        processData['tweet_tokenized'] = data_tokenized
        #Normalisasi kata gaul pada data
        data_normalized = self.__normalisasiKataGaul(processData['tweet_tokenized'])
        processData['tweet_normalized'] = data_normalized
        #list_tweet_normalized = list(processData['tweet_normalized'])
        #Stopwords Removal manual
        tweet_stopword_removed = self.__stopwordRemoval(processData['tweet_normalized'])
        processData['tweet_stopword_removed'] = tweet_stopword_removed
        #stemming
        tweet_stemmed = self.__stemming(processData['tweet_stopword_removed'])
        processData['tweet_stemming'] = tweet_stemmed

        return processData

    def __cleaningData(self, tweet_lowered):
        cleaned_tweet = []
        for x in tweet_lowered:
            # update (17/12/21): delete \\ di pattern jadi semua url terfilter
            pattern = re.compile(r'http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            pattern1 = re.compile(r'pic.twitter.com/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            pattern_nl = re.compile(r'\\n')

            #update (17/12/21) : penambahan remove new line dan rt
            #remove new line
            x = re.sub(pattern_nl,' ', x)

            #remove rt before @
            x = re.sub('(rt @)', '@',x)

            #remove urls web
            x = re.sub(pattern,' ',x)

            #remove urls pic twitter
            x = re.sub(pattern1,' ',x)

            #remove username
            x = re.sub('@[\w]+','',x)

            #Convert www.* or https?://*
            x = re.sub('((www\.[^\s]+) | (https?://[^\s]+))','',x)

            #remove number
            x = re.sub(r'\d+','',x)

            #Remove punctuation
            x = x.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))

            #Remove additional white spaces
            x = re.sub('[\s]+',' ', x)
            x = x.strip(' ')

            #Menghapus pengulangan huruf di awal maupun di akhir
            x = re.sub(r"(.)\1{2,}", r"\1"*1, x)
            cleaned_tweet.append(str(x))

        return cleaned_tweet

    #Tokenizing
    def __wordTokenizing(self, tweet_cleaned):
        return [nltk.word_tokenize(x) for x in tweet_cleaned]

    #Normalisasi Kata Gaul
    def __normalisasiKataGaul(self, tweet_tokenized):
        fSlang = pd.read_csv("./dict/colloquial.csv")
        mySlang = fSlang['slang'].tolist()
        myFormal = fSlang['formal'].tolist()
        all_normalized_reviews = []
        for x in tweet_tokenized:
            #looping kata-kata yg sudah terpisah di setiap baris
            for i, y in enumerate(x):
                if(y in mySlang):
                    x[i] = myFormal[mySlang.index(y)]
            all_normalized_reviews.append(x)
        return all_normalized_reviews

    # Stopword Removal
    def __stopwordRemoval(self, tweet_normalized):
        stopList_df = pd.read_csv('./dict/stopwordbahasa.csv', header=None)
        stopList = list(stopList_df[0])
        # nambahin stopword yang sering dipakai pada data
        stopList.extend(['ahok','djarot', 'badja','anies','sandi','agus','sylvi','agus-sylvi','anies-sandi','ahok-djarot','aniessandi','ahokdjarot','agussylvi'])
        tweet_stopword_removed = [" ".join(y for y in x if y not in stopList) for x in tweet_normalized]
        return tweet_stopword_removed
    
    #Stemming
    def __stemming(self, tweet_stopword_removed):
        stemmer = StemmerFactory().create_stemmer()
        tweet_stemmed = [stemmer.stem(x).split() for x in tweet_stopword_removed]
        return tweet_stemmed
