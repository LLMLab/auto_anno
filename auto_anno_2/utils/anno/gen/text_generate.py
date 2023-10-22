import re
from ....utils.format.txt_2_list import txt_2_list

gen_prompt = "你是一个有丰富数据的文本数据集，请帮我生成10句包含或属于以下类别的文本{类别}" \
    "\n输出格式参考：文本 | 类别" \
    "\n例如：这个东西真好 | 好评" \
    "\n{历史}" \
    "\n以下为10句类别为{类别}，且互不相关的句子："

def text_generate(type_arr, history=[]):
    from ....local_config import chat, config
    type_arr.sort(key=lambda x: len(x), reverse=True) # 从长倒短排序，有限匹配长的，防止包含短的重复匹配，如：不好，好
    history_txt = ''.join([f'{q} | {a}\n' for q, a in history])
    user = gen_prompt
    user = user.replace('{类别}', str(type_arr)).replace('{历史}', history_txt)
    content = chat(user)
    if not config['log']['silent']:
        print(f'---- text_generate ----\nuser {user}\ncontent {content}\n')
    # Check out in type_arr
    result = []
    content = re.sub(r'^\n\|', '|', content, flags=re.MULTILINE) # 防止标签换行
    content = content.replace('\n\n', '\n')
    ls = content.split('\n')
    for l in ls:
        _l = l
        has_type_arr = []
        if '|' in _l:
            _l = _l.split('|')[-1]
        for type in type_arr:
            if type in _l:
                _l = _l.replace(type, '')
                l = l.replace(f'({type})', '') # 从原文中删去类别在括号中的情况
                has_type_arr.append(type)
        # for type in has_type_arr:
        #     split_reg = '[\.,，。]'
        #     char_reg = '[^\.,，。]'
        #     l = re.sub(rf'{split_reg}{char_reg}*?{type}{char_reg}*?{split_reg}', '', l)
        l = l.replace('，属于', '|')
        l = l.split('|')[0].strip()
        l = re.sub('^[\d]+[\. 、\s]*', '', l)
        result.append([l, has_type_arr])

    return result


if __name__ == '__main__':
    # result = text_generate(['好评', '差评'])
    # result = text_generate(['有害', '无害']) # 这个类别不好生成，会有[但是]出现，同时有害无害定义不清晰
    # type_arr = txt_2_list('政治；经济；科技；文化；娱乐；民生；军事；教育；环保；其它')
    # result = text_generate(type_arr, history=[['前四个月我国外贸进出口同比增长 5.8%', ['经济']]])
    result = text_generate(['唐诗', '宋词'])
    # result = text_generate(['文明', '不文明'])
    print(result)
