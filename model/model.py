# 切记注意文件路径
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
    data_dict = {'train': '/home/aistudio/data/data283895/train.tsv',
                 'dev': '/home/aistudio/data/data283895/dev.tsv',
                 'test': '/home/aistudio/data/data283895/test.tsv'}
    with open(data_dict[mode], 'r') as f:
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
                    label, text = data[:2]  # 根据数据集 label 在第一列，text 在第二列
                    yield {"text": text, "label": label}
                elif mode == 'test':
                    text = data[1]  #  text 在第二列
                    yield {"text": text, "label": ''}

train_ds = load_dataset(read, mode="train", lazy=False)
dev_ds = load_dataset(read, mode="dev", lazy=False)
test_ds = load_dataset(read, mode="test", lazy=False)


# 构建词汇表
import jieba
from collections import defaultdict
from paddlenlp.data import Vocab
def build_vocab(texts,
                stopwords=[],
                num_words=None,
                min_freq=10,
                unk_token="[UNK]",
                pad_token="[PAD]"):
    word_counts = defaultdict(int)
    for text in texts:
        if not text:
            continue
        for word in jieba.cut(text):
            if word in stopwords:
                continue
            word_counts[word] += 1
    wcounts = []
    for word, count in word_counts.items():
        if count < min_freq:
            continue
        wcounts.append((word, count))
    wcounts.sort(key=lambda x: x[1], reverse=True)
    if num_words is not None and len(wcounts) > (num_words - 2):
        wcounts = wcounts[:(num_words - 2)]
    sorted_voc = [pad_token, unk_token]
    sorted_voc.extend(wc[0] for wc in wcounts)
    word_index = dict(zip(sorted_voc, list(range(len(sorted_voc)))))
    return word_index
texts = []
for data in train_ds:
    texts.append(data["text"])
for data in dev_ds:
    texts.append(data["text"])
stopwords = set(["的", "吗", "吧", "呀", "呜", "呢", "呗","哦","了","啊","阿"]) #停用词库
word2idx = build_vocab(
    texts, stopwords, min_freq=5, unk_token="[UNK]", pad_token="[PAD]")
vocab = Vocab.from_dict(word2idx, unk_token="[UNK]", pad_token="[PAD]")
res = vocab.to_json('/home/aistudio/model/vocab.json')


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


# 定义LSTM模型训练参数
epoch_num = 14  # 训练的迭代次数（epoch_num）
batch_size = 64  # 每次迭代的批量大小（batch_size）
learning_rate = 5e-5 # 学习率
dropout_rate = 0.2 # 正则化调控
num_layers = 1 # 网数
hidden_size = 256 
embedding_size = 256
vocab_size = len(vocab)
print(vocab_size)
model = LSTMModel(
    vocab_size,
    num_classes=2,
    emb_dim=embedding_size,
    lstm_layers=num_layers,
    direction='bidirectional',
    padding_idx=vocab['[PAD]'])
optimizer = paddle.optimizer.Adam(learning_rate=learning_rate, beta1=0.9, beta2=0.999, parameters=model.parameters())


# 训练LSTM模型
import paddle
import numpy as np
from paddle import nn
from paddle.nn import functional as F
paddle.seed(0)
np.random.seed(0)
def train(model, train_loader, optimizer, epoch_num):
    losses = []
    steps = []
    model.train()
    global_step = 0
    for epoch in range(epoch_num):
        for step, (sentences, valid_length, labels) in enumerate(train_loader):
            logits = model(sentences, valid_length) # 调用模型的 forward 方法进行前向传播，得到模型的预测输出 logits。
            loss = F.cross_entropy(input=logits, label=labels, soft_label=False)# 使用交叉熵函数计算损失，然后取平均值确保损失是一个标量。
            loss = paddle.mean(loss)  # 确保 loss 是一个标量
            loss.backward()
            optimizer.step()
            optimizer.clear_grad()
            global_step += 1
            if global_step % 100 == 0:
                losses.append(loss.item())  # 使用 .item() 来获取标量的值
                steps.append(step)
                print("epoch %d, step %d, loss %.3f" % (epoch, global_step, loss.item()))# 每 100 步记录一次损失，并打印当前的 epoch、step 和 loss。
train(model, train_loader, optimizer, epoch_num)

# 保存模型
model_name = "sentiment_classifier"
paddle.save(model.state_dict(), "/home/aistudio/model/checkpoint/{}.pdparams".format(model_name))
paddle.save(optimizer.state_dict(), "/home/aistudio/model/checkpoint/{}.pdopt".format(model_name))# 训练完成后，保存模型参数和优化器状态到文件中，以便于后续的模型恢复或评估。



# 评估模型
import paddle
import numpy as np
from paddle import nn
from paddle.nn import functional as F
@paddle.no_grad()
def evaluate(model, test_loader):
    model.eval()
    tp, tn, fp, fn = 0, 0, 0, 0
    for sentences, valid_lens, labels in test_loader:
        logits = model(sentences, valid_lens)
        probs = F.softmax(logits, axis=1)  # 确保 softmax 沿着正确的轴操作
        probs = probs.numpy()
        labels = labels.numpy()  # 确保 labels 也是 NumPy 数组
        for i in range(probs.shape[0]):
            true_label = labels[i]
            predicted_prob_positive = probs[i][1]  # 正例的概率
            predicted_label = 1 if predicted_prob_positive > 0.5 else 0
            if true_label == 1:  # 真实标签为正例
                if predicted_label == 1:
                    tp += 1  # 真正例
                else:
                    fn += 1  # 假负例
            else:  # 真实标签为负例
                if predicted_label == 1:
                    fp += 1  # 假正例
                else:
                    tn += 1  # 真负例
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    print("TP: {}\nFP: {}\nTN: {}\nFN: {}\n".format(tp, fp, tn, fn))
    print("Accuracy: %.4f" % accuracy)
state_dict = paddle.load('/home/aistudio/model/checkpoint/sentiment_classifier.pdparams')
model.load_dict(state_dict)
evaluate(model, test_loader)