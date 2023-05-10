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

input1 = gr.Textbox(lines=3, label="输入原句", value="Hello world!")
input2 = gr.Textbox(lines=3, label="输入类别", value="友好、不友好")
output = gr.Textbox(label="输出结果")
radio = gr.Radio(["文本分类", "实体抽取"], label="算法类型", value="文本分类")
checkbox = gr.Checkbox(label="翻译成中文")

if __name__ == '__main__':
  demo = gr.Interface(
    fn=auto_anno,
    description='自动标注，使用了openai免费接口，1分钟内只能请求3次，如遇报错请稍后再试，或clone项目到本地后用自己的key替换。如有疑问欢迎联系微信 maqijun123456',
    inputs=[input1, input2, radio, checkbox],
    examples=[
      ['前四个月我国外贸进出口同比增长 5.8%', '政治；经济；科技；文化；娱乐；民生；军事；教育；环保；其它', '文本分类', False],
      ['There is a cat trapped on the Avenue of Happiness', '地点', '实体抽取', True],
      ['联系方式：18812345678，联系地址：幸福大街20号', '手机号、地址', '实体抽取', False],
    ],
    outputs=[output]
  )
  demo.launch(share=False)
