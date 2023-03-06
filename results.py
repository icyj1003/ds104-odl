from river.metrics import Accuracy, MacroF1
from utils import load_object

for a in ['lstm', 'gru', 'cnn']:
    acc = load_object(f'./model/{a}/acc.pkl')
    f1 = load_object(f'./model/{a}/f1.pkl')
    print(f"{a} - Accuracy: {acc.get()}, F1Macro: {f1.get()}")
