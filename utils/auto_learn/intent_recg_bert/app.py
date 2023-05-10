'''
@license: (C) Copyright 2013-2020, Node Supply Chain Manager Corporation Limited.
@time: 2023/5/11 14:51
@file: predict.py
@author: zsc
@Software: PyCharm
@desc:
'''

from bert4keras.tokenizers import Tokenizer
from bert_model import build_bert_model
import warnings
warnings.filterwarnings("ignore")


class BertIntentModel(object):
    """
    基于bert实现的医疗意图识别模型
    """
    def __init__(self):
        super(BertIntentModel, self).__init__()
        self.dict_path = 'D:\download\Data\Bert Model\chinese_rbt3_L-3_H-768_A-12/vocab.txt'
        self.config_path = 'D:\download\Data\Bert Model\chinese_rbt3_L-3_H-768_A-12/bert_config_rbt3.json'
        self.checkpoint_path = 'D:\download\Data\Bert Model\chinese_rbt3_L-3_H-768_A-12/bert_model.ckpt'


        self.label_list  = [line.strip() for line in open("label", "r", encoding="utf8")]
        self.id2label = {idx:label for idx, label in enumerate(self.label_list)}

        self.tokenizer = Tokenizer(self.dict_path)
        self.model = build_bert_model(self.config_path, self.checkpoint_path, 13)
        self.model.load_weights("./model/best_model.weights")   # rbt3

    def predict(self, text):
        """
        对用户输入的单条文本进行预测
        :param text:
        :return:
        """
        token_ids, segment_ids = self.tokenizer.encode(text, maxlen=60)
        predict = self.model.predict([[token_ids], [segment_ids]])

        rst = {l:p for l,p in zip(self.label_list, predict[0])}
        rst = sorted(rst.items(), key= lambda kv:kv[1], reverse=True)
        intent, confidence = rst[0]
        return {"intent": intent, "confidence":float(confidence)}

if __name__ == '__main__':
    BIM = BertIntentModel()
    predict_text = "淋球菌性尿道炎的症状"
    predict_confidence = BIM.predict(predict_text)
    print(predict_text, ":", predict_confidence)

