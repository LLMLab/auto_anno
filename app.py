import gradio as gr
import json

from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
from local_config import en2cn

from utils.format.txt_2_list import txt_2_list

def file_auto_anno(file, types_txt, radio, need_trans, cls_prompt, ner_prompt):
  try:
    txts = open(file.name, 'r', encoding='utf-8').read().strip().split('\n')
  except Exception as e:
    return '请上传txt文件，其中每一行都为一句待标注原文'
  out_txts = []
  for txt in txts:
    try:
      out_anno = auto_anno(txt, types_txt, radio, need_trans, cls_prompt, ner_prompt)
      if need_trans:
        _out_anno = out_anno.split('\n')[-1]
        _txt = out_anno.replace('\n'+_out_anno, '')
        out_txt = f'{_txt}\t{_out_anno}'
      else:
        out_txt = f'{txt}\t{out_anno}'
    except Exception as e:
      out_txt = f'{txt}\t[]'
    out_txts.append(out_txt)
  return '\n'.join(out_txts)

def auto_anno(txt, types_txt, radio, need_trans, cls_prompt, ner_prompt):
  if need_trans:
    txt = en2cn(txt)
  types = txt_2_list(types_txt)
  if radio == '文本分类':
    result = text_classification(txt, types, prompt=cls_prompt)
  if radio == '实体抽取':
    result = extract_named_entities(txt, types, prompt=ner_prompt)
  if need_trans:
    result = f'{txt}\n{result}'
  return result

with gr.Blocks() as demo:
    demo.css = '#file_intput {height: 100px;}'
    with gr.Row():
        gr.Markdown("""自动标注，大模型使用了一言千帆的api，本项目开源地址为：https://github.com/LLMLab/auto_anno""")
    with gr.Row():
        with gr.Column(variant="panel"):
            input1 = gr.Textbox(lines=3, label="输入原句", value="Hello world!")
            input2 = gr.Textbox(lines=3, label="输入类别", value="友好、不友好")
            cls_prompt = gr.Textbox(lines=3, label="分类提示", value='你是一个有百年经验的文本分类器，回复以下句子的分类类别，类别选项为{类别}\n{历史}{原文}\n类别为：', visible=False)
            ner_prompt = gr.Textbox(lines=3, label="抽取提示", value='你是一个经验丰富的命名实体抽取程序。输出标准数组json格式并且标记实体在文本中的位置\n示例输入|```联系方式：18812345678，联系地址：幸福大街20号```类型[\'手机号\', \'地址\'] 输出|[{"name": "18812345678", "type": "手机号", "start": 5, "end": 16}, {"name": "幸福大街20号", "type": "地址", "start": 5, "end": 16}]\n{历史}输入|```{原文}```类型{类别}输出|', visible=False)
            radio = gr.Radio(["文本分类", "实体抽取"], label="算法类型", value="文本分类")
            checkbox = gr.Checkbox(label="翻译成中文")
            
        with gr.Column(variant="panel"):
            file1 = gr.File(label="上传文件", type="file", accept=".txt", container=False, elem_id="file_intput").style()
            output = gr.Textbox(label="输出结果", lines=3)
            # 输入输出
            inputs = [input1, input2, radio, checkbox, cls_prompt, ner_prompt]
            file_inputs = [file1, input2, radio, checkbox, cls_prompt, ner_prompt]
            with gr.Row():
              btn = gr.Button("清空").style(full_width=True)
              btn2 = gr.Button("标注", visible=True, variant="primary").style(full_width=True)
              btn3 = gr.Button("标注文件", visible=True).style(full_width=True)
              btn.click(lambda: "", [], output)
              btn2.click(auto_anno, inputs, output)
              btn3.click(file_auto_anno, file_inputs, output)
    with gr.Row():
        gr.Examples(examples=[
          ['前四个月我国外贸进出口同比增长 5.8%', '政治；经济；科技；文化；娱乐；民生；军事；教育；环保；其它', '文本分类', False],
          ['There is a cat trapped on the Avenue of Happiness', '地点', '实体抽取', True],
          ['联系方式：18812345678，联系地址：幸福大街20号', '手机号、地址', '实体抽取', False],
        ], inputs=inputs)

if __name__ == '__main__':
  demo.launch(share=False)
