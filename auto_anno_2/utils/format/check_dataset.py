import os
import json
dir_path = 'E:/NLP/NER'

fns = os.listdir(dir_path)
type_cnt_map = {}
type_types_map = {}
for fn in fns:
    if 'aa.jsonl' not in fn:
        continue
    ls = open(f'{dir_path}/{fn}', 'r', encoding='utf-8').read().strip().split('\n')
    type = fn.split('_')[1]
    if type not in type_cnt_map:
        type_cnt_map[type] = 0
    type_cnt_map[type] += len(ls)
    for l in ls:
        j = json.loads(l)
        types = j['types']
        if type not in type_types_map:
            type_types_map[type] = set()
        if '' in types:
            print(fn, l)
        type_types_map[type].update(types)
print('数据量', type_cnt_map)
print('类别数', {k: len(list(type_types_map[k])) for k in type_types_map})
