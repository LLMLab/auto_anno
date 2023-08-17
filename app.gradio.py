import gradio as gr
import json
import os
import numpy as np
import time
import re

from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
from utils.anno.gen.text_generate import text_generate
from local_config import en2cn, emb, config
from utils.format.txt_2_list import txt_2_list
from utils.format.wash import wash_tel, wash_idcard, wash_q_2_b
from utils.auto_learn.cluster_text import cluster_text

os.makedirs(f'tmp/emb/', exist_ok=True)
types_md5_vector_map = {}
emb_json_path = f'tmp/emb/{config["emb"]}.json'
if os.path.exists(emb_json_path):
  types_md5_vector_map = json.load(open(emb_json_path, 'r', encoding='utf-8'))
os.makedirs('tmp/anno/', exist_ok=True)
app_t = int(time.time())

def md5(txt):
  import hashlib
  m = hashlib.md5()
  m.update(txt.encode('utf-8'))
  return m.hexdigest()

def get_txts(file):
  if type(file) == str:
    txts = file.strip().split('\n')
  else:
    txts = open(file.name, 'r', encoding='utf-8').read().strip().split('\n')
  return txts

def get_qa(txt):
  split_key = '[\t\|]'
  qa = re.compile(split_key).split(txt)
  if len(qa) < 2:
    qa.append('')
  q = qa[0]
  a = qa[1]
  return q, a

def load_example_file(file_example, md5_vector_map):
  try:
    is_emb_update = False
    train_txts = get_txts(file_example)
    for train_txt in train_txts:
      q, a = get_qa(train_txt)
      if q not in md5_vector_map or md5_vector_map[q]['a'] != a:
        is_emb_update = True
        vector = emb(q)
        md5_vector_map[q] = {
          'vector': vector,
          'q': q,
          'a': a
        }
    if is_emb_update:
      json.dump(types_md5_vector_map, open(emb_json_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
  except Exception as e:
    print(e)
    print('已标注文件解析失败，请一行为一条数据，输入和输出用\t分割')

def load_similar_txt(txt, md5_vector_map, sample_txts):
  vector = emb(txt)
  vec_score_arr = []
  for _txt in sample_txts:
    q, _ = get_qa(_txt)
    if q not in md5_vector_map:
      continue
    vector_info = md5_vector_map[q]
    t_vector = vector_info['vector']
    similar_score = np.dot(t_vector, vector)
    vec_score_arr.append((vector_info, similar_score))
  vec_score_arr.sort(key=lambda x: x[1], reverse=True)
  history = []
  for vec_score in vec_score_arr[:4]:
    vec_info = vec_score[0]
    history.append([vec_info['q'], vec_info['a']])
  return history
# 多线程
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=30)
from tqdm import tqdm

def thread_auto_anno(out_txts, i, pbar, txt, types_txt, radio, checkbox_group, cls_prompt, ner_prompt, file_example=None):
  try:
    out_anno, txt = auto_anno(txt, types_txt, radio, checkbox_group, cls_prompt, ner_prompt, file_example=file_example)
    if radio == '无':
      out_txt = txt
    if radio == '数据生成':
      out_txt = out_anno
    else:
      out_txt = f'{txt}\t{out_anno}'
    out_txts.append([i, out_txt])
  except Exception as e:
    print('ERROR', e)
    out_txts.append([i, ''])
  pbar.update(1)
  return out_txts

def file_auto_anno(file, types_txt, radio, checkbox_group, cls_prompt, ner_prompt, file_example=None):
  sts = time.time()
  try:
    if type(file) == str:
      txts = file.strip().split('\n')
    else:
      txts = open(file.name, 'r', encoding='utf-8').read().strip().split('\n')
  except Exception as e:
    return '请输入待标注内容，其中每一行都为一句待标注原文'
  out_txts = []
  if radio == '聚类择优':
    result = cluster_text(txts, n_clusters=5)
    return '\n'.join(result)
  txts_len = len(txts)
  pbar = tqdm(total=txts_len)
  for i in range(txts_len):
    txt = txts[i]
    if radio in ['文本分类', '实体抽取']:
      txt = txt.split('\t')[0]
    # thread_auto_anno(out_txts, i, pbar, txt, types_txt, radio, checkbox_group, cls_prompt, ner_prompt, file_example=file_example)
    executor.submit(thread_auto_anno, out_txts, i, pbar, txt, types_txt, radio, checkbox_group, cls_prompt, ner_prompt, file_example=file_example)
  while len(out_txts) < txts_len:
    time.sleep(0.1)
    if time.time() - sts > 60 * 10:
      print('耗时超过10分钟，已翻译的数据已缓存，请稍后再试')
      break
  out_txts.sort(key=lambda x: x[0])
  out_txts = [f'{out_txt}' for i, out_txt in out_txts]
  return '\n'.join(out_txts)

def auto_anno(txt, types_txt, radio, checkbox_group, cls_prompt, ner_prompt, file_example=None):
  history = []
  need_trans = '翻译成中文' in checkbox_group
  need_wash_tel = '手机号脱敏' in checkbox_group
  need_wash_idcard = '身份证脱敏' in checkbox_group
  if file_example:
    types_key = f'{radio}:{types_txt}'
    if types_key not in types_md5_vector_map:
      types_md5_vector_map[types_key] = {}
    md5_vector_map = types_md5_vector_map[types_key]
    load_example_file(file_example, md5_vector_map)
    sample_txts = get_txts(file_example)
    history = load_similar_txt(txt, md5_vector_map, sample_txts)
    while len(json.dumps(history)) > 1500:
      history = history[:-1]
  if need_wash_tel:
    txt = wash_tel(txt)
  if need_wash_idcard:
    txt = wash_idcard(txt)
  if need_trans:
    # 单纯翻译 .tsv 数据集
    if radio == '无':
      cn_txt = ''
      for _txt in txt.split('\t'):
        cn = en2cn(_txt)
        cn = cn.replace('\n', ' ')
        cn_txt += cn + '\t'
      return '', cn_txt[:-1]
    else:
      txt = en2cn(txt)
  types = txt_2_list(types_txt)
  result = []
  if radio == '文本分类':
    result = text_classification(txt, types, prompt=cls_prompt, history=history)
    result = json.dumps(result, ensure_ascii=False)
  if radio == '实体抽取':
    result = extract_named_entities(txt, types, prompt=ner_prompt, history=history)
    result = json.dumps(result, ensure_ascii=False)
  if radio == '数据生成':
    result = text_generate(types, history=history)
    result = [r[0] + '\t' + json.dumps(r[1], ensure_ascii=False) for r in result]
    result = '\n'.join(result)
    txt = ''
  try:
    # 记录数据
    app_types = '、'.join(types)
    open(f'tmp/anno/{app_t}_{radio}_{app_types}.tsv', 'a', encoding='utf-8').write(f'{txt}\t{result}'.strip() + '\n')
  except:
    pass
  return result, txt

with gr.Blocks() as demo:
    demo.css = ''
    with gr.Row():
        gr.Markdown("""自动标注，大模型使用了一言千帆的api，本项目开源地址为：https://github.com/LLMLab/auto_anno""")
    with gr.Row():
        with gr.Column(variant="panel"):
            input2 = gr.Textbox(lines=3, label="输入类别", value="友好、不友好")
            cls_prompt = gr.Textbox(lines=3, label="分类提示", value='你是一个有百年经验的文本分类器，回复以下句子的分类类别，类别选项为{类别}\n{历史}输入|```{原文}```输出|', visible=False)
            ner_prompt = gr.Textbox(lines=3, label="抽取提示", value='你是一个经验丰富的命名实体抽取程序。输出标准数组json格式并且标记实体在文本中的位置\n示例输入|```联系方式：188****5678，联系地址：幸福大街20号```类型[\'手机号\', \'地址\'] 输出|[{"name": "188****5678", "type": "手机号", "start": 5, "end": 16}, {"name": "幸福大街20号", "type": "地址", "start": 5, "end": 16}]\n{历史}输入|```{原文}```类型{类别}输出|', visible=False)
            checkbox_group = gr.CheckboxGroup(["翻译成中文", "手机号脱敏", "身份证脱敏"], label="数据处理", info="")
            radio = gr.Radio(["数据生成", "聚类择优", "文本分类", "实体抽取", "无"], label="算法类型", value="文本分类")
            file_example = gr.Textbox(lines=3, label="已标注文本", value="")
            
        with gr.Column(variant="panel"):
            input1 = gr.Textbox(lines=3, label="待标注文本", value="Hello world!")
            output = gr.Textbox(label="输出结果", lines=3)
            # 输入输出
            inputs = [input1, input2, radio, checkbox_group, cls_prompt, ner_prompt, file_example]
            with gr.Row():
              btn = gr.Button("清空").style(full_width=True)
              btn2 = gr.Button("标注", visible=True, variant="primary").style(full_width=True)
              btn.click(lambda: "", [], output)
              btn2.click(file_auto_anno, inputs, output)
    with gr.Row():
        gr.Examples(examples=[
          ['前四个月我国外贸进出口同比增长 5.8%', '政治；经济；科技；文化；娱乐；民生；军事；教育；环保；其它', '文本分类', []],
          ['There is a cat trapped on the Avenue of Happiness', '地点', '实体抽取', ['翻译成中文']],
          ['联系方式：18812345678，联系地址：幸福大街20号', '手机号、地址', '实体抽取', ['手机号脱敏']],
        ], inputs=inputs)

if __name__ == '__main__':
  demo.launch(share=False)
