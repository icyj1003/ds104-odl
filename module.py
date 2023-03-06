import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np


class LSTM(nn.Module):
    def __init__(self,
                 n_features,
                 vocab_size,
                 emb_dim,
                 hid_size,
                 n_layers,
                 dropout=0.5,
                 num_classes=2):
        super(LSTM, self).__init__()
        self.emb_dim = emb_dim
        self.emb = nn.Embedding(vocab_size, emb_dim)
        self.lstm = nn.LSTM(
            emb_dim, hid_size, n_layers, dropout=dropout, batch_first=True)
        self.fc = nn.Linear(hid_size, num_classes)
        self.dropout = nn.Dropout(dropout)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, X):
        X = self.emb(X)
        output, (hn, cn) = self.lstm(X)
        hn = hn.view(-1, self.lstm.hidden_size)
        fc = self.fc(hn)
        drop = self.dropout(fc)
        return self.softmax(drop)


class GRU(nn.Module):
    def __init__(self,
                 n_features,
                 vocab_size,
                 emb_dim,
                 hid_size,
                 n_layers,
                 dropout=0.5,
                 num_classes=2):
        super(GRU, self).__init__()
        self.emb = nn.Embedding(vocab_size, emb_dim)
        self.gru = nn.GRU(
            emb_dim, hid_size, n_layers, dropout=dropout)
        self.fc = nn.Linear(hid_size, num_classes)
        self.dropout = nn.Dropout(dropout)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.emb(x)
        out, hidden = self.gru(x)
        fc = self.fc(out[:, -1])
        drop = self.dropout(fc)
        return self.softmax(drop)


class TextCNN(nn.Module):
    def __init__(self,
                 n_features,
                 vocab_size,
                 emb_dim,
                 filter_sizes,
                 num_filters,
                 num_classes=2,
                 dropout=0.5):
        super(TextCNN, self).__init__()

        self.embedding = nn.Embedding(vocab_size, emb_dim)
        self.conv1d_list = nn.ModuleList([
            nn.Conv1d(in_channels=emb_dim,
                      out_channels=num_filters[i],
                      kernel_size=filter_sizes[i],
                      padding=1)
            for i in range(len(filter_sizes))
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(np.sum(num_filters), num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x_embed = self.embedding(x)
        x_reshaped = x_embed.permute(0, 2, 1)
        x_conv_list = [F.relu(conv1d(x_reshaped))
                       for conv1d in self.conv1d_list]
        x_pool_list = [F.max_pool1d(x_conv, kernel_size=x_conv.shape[2])
                       for x_conv in x_conv_list]
        x_cat = torch.cat([x_pool.squeeze(dim=2) for x_pool in x_pool_list],
                          dim=1)
        x_fc = self.fc(x_cat)
        x_dropout = self.dropout(x_fc)
        return self.softmax(x_dropout)
