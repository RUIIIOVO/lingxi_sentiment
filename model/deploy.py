# 导入必要的库  
import paddle  
import numpy as np  
from paddle import nn  
from flask import Flask, request, jsonify  
from paddlenlp.data import JiebaTokenizer  
from paddlenlp.data import Vocab  

# 导入依赖和需要的库
import os
import random
import numpy as np
import pandas as pd
import paddle
import paddle.nn as nn
import paddle.nn.functional as F
from paddle.nn import LSTM, Embedding, Dropout, Linear
from paddlenlp.datasets import load_dataset
from paddlenlp.utils.downloader import get_path_from_url



# 数据集处理
def read(mode='train'):
    data_dict = {'train': './data/data283895/train.tsv',
                 'dev': './data/data283895/dev.tsv',
                 'test': './data/data283895/test.tsv'}
    with open(data_dict[mode], 'r', encoding='utf-8') as f:
        head = None
        for line in f.readlines():
            data = line.strip().split("\t")
            if not head:
                head = data
            else:
                if mode == 'train':
                    label, text = data
                    yield {"text": text, "label": label}
                elif mode == 'dev':
                    label, text = data[:2]  # 假设 label 在第一列，text 在第二列
                    yield {"text": text, "label": label}
                elif mode == 'test':
                    text = data[1]  # 假设 text 在第二列
                    yield {"text": text, "label": ''}

train_ds = load_dataset(read, mode="train", lazy=False)
dev_ds = load_dataset(read, mode="dev", lazy=False)
test_ds = load_dataset(read, mode="test", lazy=False)


# 加载词汇表和模型参数  
vocab_path = './vocab.json'
model_path = './checkpoint/sentiment_classifier.pdparams'
vocab = Vocab.from_json(vocab_path)  
tokenizer = JiebaTokenizer(vocab)  

# 分词与文本数据向量化
from paddlenlp.data import JiebaTokenizer
tokenizer = JiebaTokenizer(vocab)
from functools import partial
def convert_example(example, tokenizer, is_test=False):
    input_ids = tokenizer.encode(example["text"])
    valid_length = np.array(len(input_ids), dtype='int64')
    input_ids = np.array(input_ids, dtype='int64')
    if not is_test:
        label = np.array(example["label"], dtype="int64")
        return input_ids, valid_length, label
    else:
        return input_ids, valid_length
trans_fn = partial(convert_example, tokenizer=tokenizer, is_test=False)
train_ds = train_ds.map(trans_fn)
dev_ds = dev_ds.map(trans_fn)


# 数据的批处理和加载
from paddlenlp.data import Stack, Pad, Tuple
batch_size = 64
batchify_fn = lambda samples, fn=Tuple(
    Pad(axis=0, pad_val=vocab.token_to_idx.get('[PAD]', 0)),  # 表示在一个mini-batch与最长的那条数据对齐，长度不够的话用0来补齐
    Stack(dtype="int64"),  # seq len
    Stack(dtype="int64")  # label
): [data for data in fn(samples)]

train_sampler = paddle.io.BatchSampler(
    dataset=train_ds, batch_size=batch_size, shuffle=True)
test_sampler = paddle.io.BatchSampler(
    dataset=dev_ds, batch_size=batch_size, shuffle=True)
train_loader = paddle.io.DataLoader(
    train_ds, batch_sampler=train_sampler, collate_fn=batchify_fn)
test_loader = paddle.io.DataLoader(
    dev_ds, batch_sampler=test_sampler, collate_fn=batchify_fn)
 

# 定义LSTM模型
import paddlenlp as ppnlp
class LSTMModel(nn.Layer):
    def __init__(self,
                 vocab_size,
                 num_classes,
                 emb_dim=128,
                 padding_idx=0,
                 lstm_hidden_size=198,
                 direction='forward',
                 lstm_layers=1,
                 dropout_rate=0.0,
                 pooling_type=None,
                 fc_hidden_size=96):
        super().__init__()
        self.embedder = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=emb_dim,
            padding_idx=padding_idx)
        self.lstm_encoder = ppnlp.seq2vec.LSTMEncoder(
            emb_dim,
            lstm_hidden_size,
            num_layers=lstm_layers,
            direction=direction,
            dropout=dropout_rate,
            pooling_type=pooling_type)
        self.fc = nn.Linear(self.lstm_encoder.get_output_dim(), fc_hidden_size)
        self.output_layer = nn.Linear(fc_hidden_size, num_classes)
    def forward(self, text, seq_len):
        embedded_text = self.embedder(text)
        text_repr = self.lstm_encoder(embedded_text, sequence_length=seq_len)
        fc_out = paddle.tanh(self.fc(text_repr))
        logits = self.output_layer(fc_out)
        probs = F.softmax(logits, axis=-1)
        return probs
  
# 加载模型状态  
model = LSTMModel(  
    vocab_size=len(vocab),  
    num_classes=2,  
    emb_dim=256,  
    lstm_layers=1,  
    direction='bidirectional',  
    padding_idx=vocab['[PAD]']  
)  
state_dict = paddle.load(model_path)  
model.load_dict(state_dict)  
model.eval()  # 设置为评估模式  
  
# 初始化Flask应用  
app = Flask(__name__)  
  
# 定义预测函数  
@paddle.no_grad()  
def predict(text):  
    input_ids = tokenizer.encode(text)  
    input_ids = np.array(input_ids, dtype='int64').reshape([1, -1])  # 调整形状以匹配模型输入  
    valid_length = np.array([len(input_ids[0])], dtype='int64')  # 有效长度  
    logits = model(paddle.to_tensor(input_ids), paddle.to_tensor(valid_length))  
    probs = nn.functional.softmax(logits, axis=1)  
    predicted_label = np.argmax(probs.numpy(), axis=1)[0]  # 获取预测标签  
    return predicted_label  

# 设置Flask路由  
@app.route('/predict', methods=['POST'])  
def predict_route():  
    data = request.json  # 假设输入数据为JSON格式  
    text = data.get('text', '')  # 从请求中获取文本  
    label = predict(text)  # 进行预测
    return jsonify({'label': int(label)})  # 返回预测结果
  
# 运行Flask应用  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8080)  # 监听所有IP地址的8080端口