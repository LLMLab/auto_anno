import time
from tqdm import tqdm

# 读取数据
from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
from utils.api.google_trans import en2cn

def write(txt):
  with open('data/cls/jd_result.csv', 'a', encoding='utf-8') as f:
    f.write(txt)

if __name__ == '__main__':
  # 多文本分类
  txts = open('data/cls/jd.csv', 'r', encoding='utf-8').read().split('\n')[1:]
  txts = [txt.split(',')[0] for txt in txts if txt != '']

  history = [
    ['一百多和三十的也看不出什么区别，包装精美，质量应该不错。', ['好评']],
    ['太失望了，根本不值这个价', ['差评']],
    ['很不错，质量挺好的，穿着蛮舒服', ['好评']],
    ['一点也不好，我买的东西拿都拿到快递员自己签收了还不给我，恶心恶心 恶心，不要脸不要脸', ['差评']],
    ['差评，客服永远不在，四天后才发的货，衣服木有以前买的好，感觉设计比例有问题，挂肩太短勒人。', ['差评']],
    ['比较简单，适合小朋友', ['好评']],
    ['还不错，挺实用的吧。。。', ['好评']],
    ['这个字帖不错，既可以 练字，还可以看看宋词', ['好评']],
    ['买的椒盐的，结果是浓浓的奶油味，很讨厌这种浓浓的食品添加剂的味道。。', ['差评']],
    ['香气跟以前的不一样，不知道是不是假的，以前的香气很好闻。', ['差评']],
  ]
  # history = []

  results = []
  for txt in tqdm(txts):
    while True:
      try:
        result = text_classification(txt, ['好评', '差评'], history)
        results.append(result)
        write(f'{txt},{result}\n')
        break
      except Exception as e:
        print(e)
        if e.http_status == 429:
          print('等待60s...')
          time.sleep(60)
          continue
        else:
          print('等待5s...')
          time.sleep(5)
        continue
