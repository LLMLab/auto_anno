import gradio as gr
import json

from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
from utils.api.google_trans import en2cn
from utils.format.txt_2_list import txt_2_list

def auto_anno(txt, types_txt, radio, need_trans=False):
  if need_trans:
    txt = en2cn(txt)
  types = txt_2_list(types_txt)
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

if __name__ == '__main__':
  demo = gr.Interface(fn=auto_anno, inputs=[input1, input2, radio, checkbox], outputs=[output])
  demo.launch(share=False)
