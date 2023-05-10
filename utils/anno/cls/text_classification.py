import openai
import sys
import re
sys.path.append('.')
from local_config import openai_key
from utils.format.txt_2_list import txt_2_list

# Set up your API key
openai.api_key = openai_key

def text_classification(src_txt, type_arr):
    user = f"你是一个聪明而且有百年经验的文本分类器. 你的任务是从一段文本里面提取出相应的分类结果签。你的回答必须用统一的格式。文本用```符号分割。分类类型保存在一个数组里{type_arr}\n输入|```{src_txt}```输出|"
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"{user}"},
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content
    # Check out in type_arr
    result = []
    for type in type_arr:
        if type in content:
            result.append(type)
            # 删去已经匹配的type
            content = content.replace(type, '')
    return result

if __name__ == '__main__':
    # type_arr = ['好评', '差评']
    type_arr_txt = "是差评、不是差评"
    type_arr = txt_2_list(type_arr_txt)
    txts = [
        '这个商品真不错',
        '用着不行',
        '没用过这么好的东西'
    ]
    for txt in txts:
        result = text_classification(txt, type_arr)
        print(txt, result)
