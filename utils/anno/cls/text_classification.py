import sys
sys.path.append('.')
sys.path.append('auto_anno')
from utils.format.txt_2_list import txt_2_list
from utils.api.openai_api import chat

def text_classification(src_txt, type_arr, history=[], chat=chat):
    history_txt = ''.join([f'输入|```{q}```输出|{a}\n' for q, a in history])
    user = "你是一个聪明而且有百年经验的文本分类器. 你的任务是从一段文本里面提取出相应的分类结果签。你的回答必须用统一的格式。文本用```符号分割。分类类型保存在一个数组里{类别}" \
        "\n{历史}" \
        "输入|```{原文}```输出|"
    user = user.replace('{类别}', str(type_arr)).replace('{历史}', history_txt).replace('{原文}', src_txt)
    content = chat(user)
    print(content)
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
    # type_arr_txt = "是差评、不是差评"
    # type_arr_txt = "天气查询、股票查询、其他"
    type_arr_txt = '捡起、不捡'
    type_arr = txt_2_list(type_arr_txt)
    txts = [
        # '这个商品真不错',
        # '用着不行',
        # '没用过这么好的东西',
        # '今天天气怎么样',
        '地上有100块钱，但捡了会被抓起来，捡还是不捡起来？',
    ]
    history = [
        # ['这个商品真不错', ['其他']],
    ]
    for txt in txts:
        result = text_classification(txt, type_arr, history)
        print(txt, result)
