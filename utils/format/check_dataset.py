import os
dir_path = 'E:/NLP/NER'

fns = os.listdir(dir_path)
type_cnt_map = {}
for fn in fns:
    if 'aa.jsonl' not in fn:
        continue
    ls = open(f'{dir_path}/{fn}', 'r', encoding='utf-8').read().strip().split('\n')
    type = fn.split('_')[1]
    if type not in type_cnt_map:
        type_cnt_map[type] = 0
    type_cnt_map[type] += len(ls)
print(type_cnt_map)
