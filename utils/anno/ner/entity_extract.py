import json
import sys
import re
from ....local_config import config

ner_prompt = "你是一个聪明而且有百年经验的命名实体识别（NER）识别器. 你的任务是从一段文本里面提取出相应的实体并且给出标签。你的回答必须用统一的格式。文本用```符号分割。输出采用Json的格式并且标记实体在文本中的位置。实体类型保存在一个数组里{类别}\n" \
        '\n输入|```皮卡丘神奇宝贝```输出|[{"name": "皮卡丘", "type": "Person", "start": 0, "end": 3}, {"name": "神奇宝贝", "type": "物种", "start": 4, "end": 8}]' \
        "\n{历史}" \
        "输入|```{原文}```输出|"

def get_ready_key(name, type, start):
    return f'{name}-{type}-{start}'

def extract_named_entities(src_txt, type_arr, history=[], chat=None, prompt=ner_prompt):
    if not chat:
        from ....local_config import chat
    history_txt = ''.join([f'输入|```{q}```输出|{json.dumps(a, ensure_ascii=False)}\n' for q, a in history])
    user = prompt
    user = user.replace('{类别}', str(type_arr)).replace('{历史}', history_txt).replace('{原文}', src_txt)
    content = chat(user)    
    if not config['log']['silent']:
        print(f'---- extract_named_entities ----\nuser {user}\ncontent {content}\n')
    # 跨行替换
    content = re.sub(r'\][^紒]*', ']', content)
    content = re.sub(r'[^紒]*\[', '[', content)
    content = re.sub(r'\\', '', content)
    j = json.loads(content)
    result = []
    j.sort(key=lambda x: x['start']*1000+x['end'])
    ready_keys = set()
    for item in j:
        s = item['start']
        e = item['end']
        # 过滤非目标实体类型
        if not type_arr.__contains__(item['type']):
            continue
        # 修正标注错误的实体坐标
        if src_txt[s:e] != item['name']:
            for i in range(len(src_txt)):
                if src_txt[i:i+len(item['name'])] != item['name']:
                    continue
                # 跳过匹配过的实体，防止重复匹配
                ready_key = get_ready_key(item['name'], item['type'], i)
                if ready_keys.__contains__(ready_key):
                    continue
                item['start'] = i
                break
        # 确保实体结尾坐标正确
        item['end'] = item['start'] + len(item['name'])
        # 将在实体类型里的放入结果
        result.append(item)
        ready_key = get_ready_key(item['name'], item['type'], item['start'])
        ready_keys.add(ready_key)
    return result

if __name__ == '__main__':
    # extract_named_entities("```汤姆每天都被杰瑞欺负，皮卡丘越来越想帮忙，竟然还总是被拒绝，心想难道我“皮大仙”这点能力都没有？而且，这货不是被虐狂吧```", ["Person", "物种"])
    result = extract_named_entities('老百姓心新乡新闻网话说这几天新乡天气还好吧偷笑', ['代称', '行政区'])
    print(result)
