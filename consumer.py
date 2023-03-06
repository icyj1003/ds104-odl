import time
import uuid
from bytewax.inputs import KafkaInputConfig
from bytewax.outputs import ManualOutputConfig
from bytewax.execution import run_main
from bytewax.dataflow import Dataflow
from river.metrics import Accuracy, MacroF1
from create_dataset import Vocabulary
from deep_river.classification import Classifier
from preprocess import clean
from utils import load_object, pad_sentence, save_object, vector_to_dict
import json
import pickle
from pymongo import MongoClient


def output_builder(wi, wc):
    connect_url = "mongodb+srv://noticy:yexx2YId6UUCFnR8@cluster0.mlaq4tt.mongodb.net/odl?retryWrites=true&w=majority"
    cluster = MongoClient(connect_url)
    db = cluster['odl']
    collection = db['post']

    def output_handler(data):
        if data:
            collection.insert_one(data)
            time.sleep(1)

    return output_handler


# load model
a = 'cnn'
model = load_object(f'C:/Users/ADMIN/Desktop/odl/model/{a}/model.pkl')
vocab = load_object('C:/Users/ADMIN/Desktop/odl/dataset/vocab.pkl')


legits = ['Thông tin Chính phủ',
          'Trung tâm Tin tức VTV24',
          'Trường Đại học Công nghệ Thông tin - Đại học Quốc gia TP.HCM',
          'Báo Thanh Niên',
          'Đại học Quốc gia TP.HCM',
          ]

scams = ['Group Giao Lưu BnS',
         'Bestie'
         ]


def handling(message):

    key, value = message

    key = json.loads(key)
    value = json.loads(value)

    tokens = clean(value['content'])

    # Những page chính thống
    if value['user'] in legits or value['user'] in scams:

        if value['user'] in legits:
            label = 0
        else:
            label = 1

        # update vocab
        vocab.from_sentence(tokens)

        # padding
        vector = pad_sentence(vocab.sentence_to_vector(tokens), 50)
        v2d = vector_to_dict(vector)

        # update metrics
        accuracy = load_object(f'C:/Users/ADMIN/Desktop/odl/model/{a}/acc.pkl')
        f1 = load_object(f'C:/Users/ADMIN/Desktop/odl/model/{a}/f1.pkl')
        y_pred = model.predict_one(v2d)
        f1 = f1.update(label, y_pred)
        accuracy = accuracy.update(label, y_pred)

        # học một điểm dữ liệu
        model.learn_one(v2d, label)
        print(f"learned {tokens} {label}")

        # save model and vocab and metrics
        with open(f'C:/Users/ADMIN/Desktop/odl/model/{a}/model.pkl', 'wb') as f:
            pickle.dump(model, f)
        save_object(
            vocab, 'C:/Users/ADMIN/Desktop/odl/dataset/', 'vocab.pkl')
        save_object(
            accuracy, f'C:/Users/ADMIN/Desktop/odl/model/{a}', 'acc.pkl')
        save_object(
            f1, f'C:/Users/ADMIN/Desktop/odl/model/{a}', 'f1.pkl')

        return {
            '_id': str(uuid.uuid4()),
            'content': ' '.join(tokens),
            'user': value['user'],
            'timestamp': value['timestamp'],
            'label': label,

        }
    else:
        vector = pad_sentence(vocab.sentence_to_vector(tokens), 50)
        return {
            '_id': str(uuid.uuid4()),
            'content': ' '.join(tokens),
            'user': value['user'],
            'timestamp': value['timestamp'],
            'label': model.predict_one(vector_to_dict(vector=vector)),

        }


flow = Dataflow()
flow.input("inp", KafkaInputConfig(brokers=['localhost:9092'], topic='post'))
flow.map(handling)
flow.capture(ManualOutputConfig(output_builder))

run_main(flow)
