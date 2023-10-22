'''
@license: (C) Copyright 2013-2020, Node Supply Chain Manager Corporation Limited.
@time: 2023/5/11 14:51
@file: predict.py
@author: zsc
@Software: PyCharm
@desc:
'''
from bert4keras.snippets import sequence_padding, DataGenerator
from data_helper import load_data
from bert4keras.tokenizers import Tokenizer
from bert_model import build_bert_model
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# config
maxlen = 128
batch_size = 8
config_path = 'D:\download\Data\Bert Model\chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = 'D:\download\Data\Bert Model\chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = 'D:\download\Data\Bert Model\chinese_L-12_H-768_A-12/vocab.txt'
tokenizer = Tokenizer(dict_path)
class_nums = 13


def predict(text):
    """
    输入单个文本进行预测
    :param text:
    :return:
    """
    model = build_bert_model(config_path, checkpoint_path, class_nums)
    model.load_weights('./model/best_model_weights')
    token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
    predict_result = model.predict([[token_ids], [segment_ids]])
    label_list = [line.strip() for line in open("label", "r", encoding="utf8")]
    rst = {l: p for l, p in zip(label_list, predict_result[0])}
    rst = sorted(rst.items(), key=lambda kv: kv[1], reverse=True)
    intent, confidence = rst[0]

    return text, intent, confidence

def predict_csv():
    """
    预测多个文本
    :param text:
    :return:
    """
    df = pd.read_csv('data/test_data.csv')
    texts = df['text'].tolist()
    data = []
    for text in texts:
        tri = predict(text)
        data.append(tri)
    df = pd.DataFrame(data, columns=['text', 'label', 'threshold'])
    df = df.sort_values('threshold', ascending=True)
    df.to_csv('output_sort.csv', index=False)
    df = pd.read_csv('output_sort.csv')
    df = df.iloc[:int(len(df)*0.2)]
    df.to_csv('output_low_confidence.csv', index=False)

if __name__ == '__main__':
    print("please wait for a moment")
    predict_csv()
    print("ok")