import json
import re
from tqdm import tqdm

cnt = 0
instruction_regs = [
    # 关系抽取
    # r'我将给你个输入，请根据关系列表：(.*?)，从输入中抽取出可能包含的关系三元组，并以(.*?)的形式回答。',
    # r'我希望你根据关系列表从给定的输入中抽取可能的关系三元组，并以(.*?)的格式回答，关系列表=(.*?)。',
    # r'给定的关系列表是：(.*?)\n根据关系列表抽取关系三元组，在这个句子中可能包含哪些关系三元组？请以(.*?)的格式回答。',
    # r'已知候选的关系列表：(.*?)，请你根据关系列表，从以下输入中抽取出可能存在的头实体与尾实体，并给出对应的关系三元组。请按照(.*?)的格式回答。'
    # '从给定的文本中提取出可能的实体和实体类型',
    # 实体抽取
    r'给定的实体类型列表是(.*?)\n根据实体类型列表抽取，在这个句子中可能包含哪些实体？你可以先别出实体, 再判断实体类型。请以(.*?)的格式回答。',
    r'我希望你根据实体类型列表从给定的输入中抽取可能的实体，并以(.*?)的格式回答，实体类型列表=(.*?)。',
    r'我将给你个输入，请根据实体类型列表：(.*?)，从输入中抽取出可能包含的实体，并以(.*?)的形式回答。',
    r'已知候选的实体类型列表：(.*?)，请你根据实体类型列表，从以下输入中抽取出可能存在的实体。请按照(.*?)的格式回答。',
]

out_output_reg_map = {
    "JSON字符串[{'entity':'', 'entity_type':''}, ]": r"{'entity': '(.*?)', 'entity_type': '(.*?)'}",
    '"实体是\n实体类型是\n\n"': r'实体是(.*?)\n实体类型是(.*?)\n\n',
    '"实体：实体类型\n"': r'(.*?)：(.*?)\n',
    '"(实体,实体类型)"': r'\((.*?),(.*?)\)'
}

def get_ready_key(name, type, start):
    return f'{name}-{type}-{start}'

def get_kvs_json(kvs, text):
    annos = []
    ks = set()
    for k in kvs:
        vs = kvs[k]
        if type(vs) == str:
            vs = [vs]
        for v in vs:
            if v in text:
                ks.add(k)
                annos.append([v, k, text.index(v)])
    return list(ks), annos

def llm_2_json(fn):
    ls = open(fn, 'r', encoding='utf-8').read().strip().split('\n')
    fh = open(re.sub(r'\..*', '.aa.jsonl', fn), 'w', encoding='utf-8')
    input_set = set()
    type_set = set()
    for l in tqdm(ls):
        j = json.loads(l)
        input = j['input']
        is_in = False
        for i in instruction_regs:
            results = re.findall(i, j['instruction'], re.S)
            if results:
                result = results[0]
                if result[0][0] == '[':
                    types, out_format = eval(result[0]), result[1]
                else:
                    types, out_format = eval(result[1]), result[0]
                
                annos = []
                match_times = 0
                output_reg = out_output_reg_map[out_format]
                output = j['output'].replace('输入中包含的实体是：\n', '')
                annos = re.findall(output_reg, output, re.S)
                # 因为原始数据为 姓名：NAN，说明数据错了，所以转回来
                if out_format == '"实体：实体类型\n"':
                    annos = [(item[1], item[0]) for item in annos]
                # 把没有结果的实体去掉
                annos = [item for item in annos if item[0] != 'NAN']
                # 补充实体位置
                _annos = []
                ready_keys = set()
                for anno in annos:
                    for i in range(len(input)):
                        if input[i:i+len(anno[0])] != anno[0]:
                            continue
                        # 跳过匹配过的实体，防止重复匹配
                        ready_key = get_ready_key(anno[0], anno[1], i)
                        if ready_keys.__contains__(ready_key):
                            continue
                        ready_keys.add(ready_key)
                        _annos.append([anno[0], anno[1], i])
                        break
                annos = _annos
                if annos:
                    match_times += 1
                    # print(annos)
                is_in = True
                continue
        j = {
            'types': types,
            'annos': annos,
            'input': input,
        }
        type_set.update(types)
        input_set.add(j['input'])
        fh.write(json.dumps(j, ensure_ascii=False) + '\n')
        if not annos:
            # print(j['output'])
            pass
        if not is_in:
            cnt += 1
            print(j['instruction'])
            pass
    print(len(input_set))
    print(len(type_set))

def json_2_json(fn, trans_fun, ls_fun=None):
    src = open(fn, 'r', encoding='utf-8').read().strip()
    if ls_fun:
        ls = ls_fun(src)
    elif src[0] == '[':
        ls = json.loads(src)
    else:
        ls = src.split('\n')
    out_ls = []
    out_js = []
    for l in ls:
        if type(l) == str:
            j = json.loads(l)
        else:
            j = l
        out_j = {
            'types': trans_fun['types'](j),
            'annos': trans_fun['annos'](j),
            'input': trans_fun['input'](j),    
        }
        out_ls.append(json.dumps(out_j, ensure_ascii=False))
        out_js.append(out_j)
    open(re.sub(r'\..*', '.aa.jsonl', fn), 'w', encoding='utf-8').write('\n'.join(out_ls))
    return out_js
        

if __name__ == "__main__":
    import random

    # fn = 'E:/NLP/NER/KnowLM-IE.json'
    # fn = 'E:/NLP/NER/48_ner_knowlm-ke_ner_train.json'
    # llm_2_json(fn)
    # fn = 'E:/NLP/NER/03_ner_yidu_s4k_subtask1_training_part.json'
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: list(set([entity['label_type'] for entity in j['entities']])),
    #     'annos': lambda j: [[j['originalText'][entity['start_pos']:entity['end_pos']] , entity['label_type'], entity['start_pos']] for entity in j['entities']],
    #     'input': lambda j: j['originalText'],
    # })
    # fn = 'E:/NLP/NER/05_ner_medical_ner_entities.json'
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: list(set([entity['label'] for entity in j['annotations']])),
    #     'annos': lambda j: [[entity['entity'] , entity['label'], entity['start_offset']] for entity in j['annotations']],
    #     'input': lambda j: j['text'],
    # })
    # fn = 'E:/NLP/NER/06_ner_MedDG_train.json'
    # types = 'Symptom Medicine Test Attribute Disease'.split(' ')
    # def get_annos(j):
    #     annos = []
    #     for type in types:
    #         if j[type]:
    #             for entity in j[type]:
    #                 if entity in j['Sentence']:
    #                     annos.append([entity, type, j['Sentence'].index(entity)])
    #     return annos
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: types,
    #     'annos': lambda j: get_annos(j),
    #     'input': lambda j: j['Sentence'],
    # }, ls_fun=lambda src: sum(json.loads(src), []))
    # fn = 'E:/NLP/NER/38_ner_COTE_train.tsv'
    # types = ['评价对象']
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: types,
    #     'annos': lambda j: [[j[0], '评价对象', j[1].index(j[0])]] if len(j) == 2 and j[0] in j[1] else [],
    #     'input': lambda j: j[1],
    # }, ls_fun=lambda src: [l.split('\t') for l in src.split('\n')][1:])
    # fn = 'E:/NLP/NER/44_ner_guwenee.json'
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: list(set([arg['role'] for arg in sum([event['arguments'] for event in j['event_list']], [])])),
    #     'annos': lambda j: [[arg['argument'], arg['role'], j['text'].index(arg['argument'])] for arg in sum([event['arguments'] for event in j['event_list']], [])],
    #     'input': lambda j: j['text'],
    # })
    # fn = 'E:/NLP/NER/20_ner_odkg_document.json'
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: get_kvs_json(json.loads(json.loads(j['业务抽取'])), j['正文'])[0],
    #     'annos': lambda j: get_kvs_json(json.loads(json.loads(j['业务抽取'])), j['正文'])[1],
    #     'input': lambda j: j['正文'],
    # })
    fn = 'E:/NLP/NER/32_ner_event_type_entity_extract_train.csv'
    types = ['涉嫌传销', '资金账户风险', '财务造假', '失联跑路', '涉嫌欺诈', '重组失败', '资产负面', '产品违规', '业绩下滑', '不能履职', '歇业停业', '公司股市异常', '信批违规', '高管负面', '提现困难', '其他', '实控人股东变更', '投诉维权', '涉嫌违法', '涉嫌非法集资', '评级调整', '交易违规']
    out_js = json_2_json(fn, trans_fun={
        'types': lambda j: [j[-2]],
        'annos': lambda j: [[j[-1], j[-2], j[1].index(j[-1])]] if j[-1] in j[1] else [],
        'input': lambda j: j[1],
    }, ls_fun=lambda src: [l[1:-1].split('","') for l in src.split('\n')])
    # types = list(set(sum([j['types'] for j in out_js], [])))
    
