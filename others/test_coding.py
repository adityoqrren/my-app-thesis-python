word = "saya adityo aji pambudi mahasiswa teknik informatika bilingual 2017"

vocal_dict = {}

vocal_words = ['a','i','u','e','o']

for i in word:
    if i in vocal_words:
        if i in vocal_dict:
            vocal_dict[i] = vocal_dict[i] + 1
        else:
            vocal_dict[i] = 1

print(vocal_dict)