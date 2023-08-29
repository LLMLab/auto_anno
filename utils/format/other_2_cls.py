import json
import re
from tqdm import tqdm

input_set = set()
type_set = set()

def strip_csv(src):
    if src and src[0] == '"' and src[-1] == '"':
        return src[1:-1]
    return src

def get_j(j):
    annos = [row['value']['choices'][0] for row in j['annotations'][0]['result']]
    input = j['data']['text']
    return annos, input

# ls = open(fn, 'r', encoding='utf-8').read().strip().split('\n')
# ls = ls[1:]
def json_2_json(fn, trans_fun=None, ls_fun=None):
    src = open(fn, 'r', encoding='utf-8').read().strip()
    if ls_fun:
        ls = ls_fun(src)
    elif src[0] == '[':
        ls = json.loads(src)
    else:
        ls = src.split('\n')
    fh = open(re.sub(r'\..*', '.aa.jsonl', fn), 'w', encoding='utf-8')
    for l in tqdm(ls):
        j = l
        out_j = {
            'types': trans_fun['types'](j),
            'annos': trans_fun['annos'](j),
            'input': trans_fun['input'](j),
        }
        fh.write(json.dumps(out_j, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    
    fn = 'E:/NLP/NER/54_cls_ChnSentiCorp_htl_all.csv'
    types = ['负面', '正面']
    json_2_json(fn, trans_fun={
        'types': lambda j: types,
        'annos': lambda j: types[j[0]],
        'input': lambda j: j[1],
    }, ls_fun=lambda src: [[int(l[0]), strip_csv(l[2:])] for l in src.strip().split('\n')[1:]])
    # fn = 'E:/NLP/NER/01_cls_label_studio.json'
    # types = '病情诊断\n治疗方案\n病因分析\n指标解读\n就医建议\n疾病表述\n后果表述\n注意事项\n功效作用\n医疗费用\n其他'.split('\n')
    # json_2_json(fn, trans_fun={
    #     'types': lambda j: types,
    #     'annos': lambda j: [row['value']['choices'][0] for row in j['annotations'][0]['result']],
    #     'input': lambda j: j['data']['text'],
    # })
