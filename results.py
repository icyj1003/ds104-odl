from river.metrics import Accuracy, MacroF1
from utils import load_object
import pandas as pd

model = ['lstm', 'gru', 'cnn']
acc_list = []
f1_list = []

for a in model:
    acc = load_object(f'./model/{a}/acc.pkl')
    f1 = load_object(f'./model/{a}/f1.pkl')
    c1 = acc.get()
    c2 = f1.get()
    acc_list.append(c1)
    f1_list.append(c2)
    print(f"{a} - Accuracy: {c1}, F1Macro: {c2}")

df = pd.DataFrame(data={'model': model, 'acc': acc_list, 'f1-macro': f1_list})
df.to_csv('./resources/results.csv', index=False)
