from river import metrics
from deep_river.classification import Classifier
from module import GRU, LSTM, TextCNN
from tqdm import tqdm
import torch
import random
import pickle
from utils import load_object, vector_to_dict, save_object
import warnings
from create_dataset import Vocabulary

warnings.filterwarnings("ignore")

# define arch
model_arc = 'lstm'

# define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

# define dataset
X = load_object('C:/Users/ADMIN/Desktop/odl/dataset/x_train.pkl')
y = load_object('C:/Users/ADMIN/Desktop/odl/dataset/y_train.pkl')
vocabulary = load_object('C:/Users/ADMIN/Desktop/odl/dataset/vocab.pkl')

dataset = []

for x, y in zip(X, y):
    dataset.append((vector_to_dict(x), y))

# random.shuffle(dataset)

# define model pipeline
if model_arc in ["lstm", 'gru']:
    if model_arc == "lstm":
        model = Classifier(module=LSTM,
                           loss_fn="binary_cross_entropy",
                           optimizer_fn='adam',
                           device='cuda',
                           emb_dim=100,
                           hid_size=128,
                           n_layers=1,
                           vocab_size=100000)
    else:
        model = Classifier(module=GRU,
                           loss_fn="binary_cross_entropy",
                           optimizer_fn='adam',
                           device='cuda',
                           emb_dim=100,
                           hid_size=128,
                           n_layers=1,
                           vocab_size=100000)
else:
    model = Classifier(module=TextCNN,
                       loss_fn="binary_cross_entropy",
                       optimizer_fn='adam',
                       device='cuda',
                       emb_dim=100,
                       filter_sizes=[3, 4, 5],
                       num_filters=[100, 100, 100],
                       vocab_size=100000)

# define metric
accuracy = metrics.Accuracy()
f1 = metrics.MacroF1()


# training procecss
for x, y in tqdm(dataset[:], leave=True,
                 desc=f"Looping",
                 unit=' samples'):
    y_pred = model.predict_one(x)
    y_proba = model.predict_proba_one(x)

    # update metric
    f1 = f1.update(y, y_pred)
    accuracy = accuracy.update(y, y_pred)
    # make the model learn
    model.learn_one(x, y)

print(f'Accuracy: {accuracy.get()}, F1Macro: {f1.get()}')


# save model and metrics
with open(f'C:/Users/ADMIN/Desktop/odl/model/{model_arc}/model.pkl', 'wb') as f:
    pickle.dump(model, f)

save_object(
    accuracy, f'C:/Users/ADMIN/Desktop/odl/model/{model_arc}', 'acc.pkl')
save_object(
    f1, f'C:/Users/ADMIN/Desktop/odl/model/{model_arc}', 'f1.pkl')
