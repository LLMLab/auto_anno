import openai
import sys
sys.path.append('.')
from local_config import openai_key

# Set up your API key
openai.api_key = openai_key

def text_classification(src_txt, type_arr):
    system = f"你是一个聪明而且有百年经验的文本. 你的任务是从一段文本里面提取出相应的分类结果签。你的回答必须用统一的格式。文本用```符号分割。分类类型保存在一个数组里{type_arr}"
    user = f"输入|```这个商品真垃圾```输出|"
    assistant = "差评"
    input = f"输入|```{src_txt}```输出|"
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"{system}"},
                        {"role": "user", "content": f"{user}"},
                        {"role": "assistant", "content": f"{assistant}"},
                        {"role": "user", "content": f"{input}"}
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content
    return content

if __name__ == '__main__':
    type_arr = ['好评', '差评']
    txts = [
        '这个商品真不错',
        '用着不行',
        '没用过这么好的东西'
    ]
    for txt in txts:
        result = text_classification(txt, type_arr)
        print(txt, result)
