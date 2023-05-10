import gradio as gr
import json

def auto_anno(txt, types, radio, need_trans=False):
  if need_trans:
    txt = en2cn(txt)
  if radio == '文本分类':
    result = text_classification(txt, types)
  if radio == '实体抽取':
    result = extract_named_entities(txt, types)
  if need_trans:
    result = f'{txt}\n{result}'
  return result

input1 = gr.Textbox(lines=3, label="输入原句")
input2 = gr.Textbox(lines=3, label="输入类别")
output = gr.Textbox(label="输出结果")
radio = gr.Radio(["文本分类", "实体抽取"], label="算法类型")
checkbox = gr.Checkbox(label="翻译成中文")

# 读取数据
from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
from utils.api.google_trans import en2cn

if __name__ == '__main__':
  # # 多文本分类
  # txts = open('data/cls/jd.csv', 'r', encoding='utf-8').read().split('\n')[1:]
  # txts = [txt.split(',')[0] for txt in txts if txt != '']

  # results = []
  # for txt in txts:
  #   results.append(text_classification(txt, ['好评', '差评']))
  demo = gr.Interface(fn=auto_anno, inputs=[input1, input2, radio, checkbox], outputs=[output])
  demo.launch(share=True)
