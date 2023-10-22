import requests

def auto_anno(text, types, algo_type):
  try:
    response = requests.post("https://aistudio.baidu.com/serving/app/4639/run/predict", json={
      "data": [
        text,
        types,
        algo_type,
        False,
        "你是一个有百年经验的文本分类器，回复以下句子的分类类别，类别选项为{类别}\n{历史}{原文}\n类别为：",
        '''你是一个经验丰富的命名实体抽取程序。输出标准数组json格式并且标记实体在文本中的位置\n示例输入|```联系方式：18812345678，联系地址：幸福大街20号```类型['手机号', '地址'] 输出|[{"name": "18812345678", "type": "手机号", "start": 5, "end": 16}, {"name": "幸福大街20号", "type": "地址", "start": 5, "end": 16}]\n{历史}输入|```{原文}```类型{类别}输出|''',
      ]
    })

    data = response.json()["data"]
    return data[0]
  except Exception as e:
    print(e)
    return ''

import json
def test_ner():
  # text = "联系方式：18812345678，联系地址：幸福大街20号"
  # types = ["手机号", "地址"]
  # algo_type = "实体抽取"
  # data = auto_anno(text, types, algo_type)
  # print(data)
  ls = open(r'C:\Users\Maxmon\Desktop\auto_anno\data\medical\CMeIE_train.jsonl', 'r', encoding='utf-8').read().strip().split('\n')
  out = ''
  for l in ls[:10]:
    j = json.loads(l)
    data = auto_anno(j['prompt'], '、'.join(['疾病', '检查', '药物']), '实体抽取')
    print(data)
    out += data + '\n'
  open(r'C:\Users\Maxmon\Desktop\auto_anno\data\medical\CMeIE_train_out.jsonl', 'w', encoding='utf-8').write(out)

def test_cls():
  text = "今天天气不错"
  types = ["正面", "负面"]
  algo_type = "文本分类"
  data = auto_anno(text, types, algo_type)
  print(data)

if __name__ == "__main__":
  test_ner()
  # test_cls()
