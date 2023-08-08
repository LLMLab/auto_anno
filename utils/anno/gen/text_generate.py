import re
import sys
sys.path.append('.')
sys.path.append('auto_anno')
from utils.format.txt_2_list import txt_2_list
from local_config import chat

gen_prompt = "你是一个有丰富数据的文本数据集，请帮我生成10句包含或属于以下类别的文本{类别}" \
    "\n输出格式参考：文本|类别" \
    "\n{历史}" \
    "\n以下为10句互不相关的句子："

def text_generate(type_arr, history=[]):
    history_txt = ''.join([f'{q} | {a}\n' for q, a in history])
    user = gen_prompt
    user = user.replace('{类别}', str(type_arr)).replace('{历史}', history_txt)
    print('user', user)
    content = chat(user)
    print('content', content)
    # Check out in type_arr
    result = []
    content = re.sub(r'^\n\|', '|', content, flags=re.MULTILINE) # 防止标签换行
    ls = content.split('\n')
    for l in ls:
        has_type_arr = []
        for type in type_arr:
            if type in l:
                has_type_arr.append(type)
        # for type in has_type_arr:
        #     split_reg = '[\.,，。]'
        #     char_reg = '[^\.,，。]'
        #     l = re.sub(rf'{split_reg}{char_reg}*?{type}{char_reg}*?{split_reg}', '', l)
        for type in has_type_arr:
            l = l.replace('，属于', '|')
            l = l.split('|')[0].strip()
        l = re.sub('^[\d]+[\. 、\s]*', '', l)
        result.append([l, has_type_arr])

    return result


if __name__ == '__main__':
    # text_generate(['好评', '差评'])
    # text_generate(['有害', '无害']) # 这个类别不好生成，会有[但是]出现，同时有害无害定义不清晰
    type_arr = txt_2_list('政治；经济；科技；文化；娱乐；民生；军事；教育；环保；其它')
    text_generate(type_arr, history=[['前四个月我国外贸进出口同比增长 5.8%', ['经济']]])
