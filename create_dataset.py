from tqdm import tqdm
from preprocess import clean
import pandas as pd
import json
from utils import pad_sentence, save_object
from sklearn.model_selection import train_test_split


class Vocabulary:
    def __init__(self, default_indexes={}):
        self.default_indexes = {**default_indexes}
        self.init()

    def init(self):
        self.index_to_word = {**self.default_indexes}
        self.word_to_index = {}
        self.word_counts = {}
        self.num_words = len(self.default_indexes)
        for idx, word in self.index_to_word.items():
            self.word_to_index[word] = idx

    def from_sentence(self, word_list):
        for word in word_list:
            self.from_word(word)

    def from_word(self, word, cnt=None):
        if word not in self.word_to_index:
            self.index_to_word[len(self.index_to_word)] = word
            self.word_to_index[word] = len(self.word_to_index)
            if cnt is None:
                self.word_counts[word] = 1
                self.num_words += 1
            else:
                self.word_counts[word] = cnt
                self.num_words += cnt
        else:
            if cnt is None:
                self.word_counts[word] += 1
            else:
                self.word_counts[word] += cnt

    def vector_to_sentence(self, indices):
        return [self.index_to_word[int(i)] if int(i) in self.index_to_word else None for i in indices]

    def sentence_to_vector(self, sen):
        idxs = [self.word_to_index[word]
                if word in self.word_to_index else 1 for word in sen]
        return idxs

    def save_indexes(self, directory):
        if not directory.endswith('/'):
            directory = directory + '/'

        with open(directory + "vocab.json", "w", encoding='utf8') as file:
            json.dump(self.index_to_word, file, ensure_ascii=False)


class CustomDataset():
    def __init__(self, X, y, max_len, vocabulary):
        self.X = [pad_sentence(vocabulary.sentence_to_vector(
            sen), max_len=max_len) for sen in X]
        self.y = y

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.y)


if __name__ == '__main__':
    print('Đọc dữ liệu...')
    df = pd.read_csv('C:/Users/ADMIN/Desktop/odl/reintel2020/public_train.csv')

    X = df.post_message.values.tolist()
    y = df.label.values.tolist()

    print('Tiền xử lý dữ liệu...')
    X = [clean(str(sen)) for sen in tqdm(X)]

    print('Tạo tập từ vựng...')
    vocabulary = Vocabulary(default_indexes={0: '<pad>', 1: '<unk>'})

    for sen in X:
        vocabulary.from_sentence(sen)

    print('word -> vector')
    X = [pad_sentence(vocabulary.sentence_to_vector(
        sen), max_len=50) for sen in tqdm(X)]
    print('Lưu dataset')

    save_object(vocabulary, 'C:/Users/ADMIN/Desktop/odl/dataset/', 'vocab.pkl')
    save_object(X, 'C:/Users/ADMIN/Desktop/odl/dataset/', 'x_train.pkl')
    save_object(y, 'C:/Users/ADMIN/Desktop/odl/dataset/', 'y_train.pkl')

    print('Xong!')
    print(vocabulary.num_words)
    print(vocabulary.index_to_word)
