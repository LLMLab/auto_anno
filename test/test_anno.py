import time
from tqdm import tqdm

# 读取数据
from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
from utils.auto_learn.cluster_text import cluster_text

def write(txt):
  with open('data/cls/jd_result.csv', 'a', encoding='utf-8') as f:
    f.write(txt)

if __name__ == '__main__':
  import json
  # # 多文本分类
  # txts = open('data/cls/jd.csv', 'r', encoding='utf-8').read().split('\n')[1:]
  # txts = [txt.split(',')[0] for txt in txts if txt != '']

  # 读取数据
  fpath = 'data/LLMLab_CLS_NER.984k.v1/01_cls_label_studio.aa.jsonl'
  # fpath = 'data/LLMLab_CLS_NER.984k.v1/03_ner_yidu_s4k_subtask1_training_part.ab.jsonl'
  txts = open(fpath, 'r', encoding='utf-8').read().strip().split('\n')[:100]

  for txt in txts:
    j = json.loads(txt)
    result = text_classification(j['input'], j['types'])
    print('P' if str(j['annos']) == str(result) else '_', j['annos'], result)

  results = cluster_text(txts, n_clusters=10)
  print(results)
  
