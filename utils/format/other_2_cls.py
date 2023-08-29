import json
import re
from tqdm import tqdm

# fn = 'E:/NLP/NER/54_cls_ChnSentiCorp_htl_all.csv'
# types = ['负面', '正面']
fn = 'E:/NLP/NER/01_cls_label_studio.json'
types = '病情诊断\n治疗方案\n病因分析\n指标解读\n就医建议\n疾病表述\n后果表述\n注意事项\n功效作用\n医疗费用\n其他'.split('\n')

fh = open(re.sub(r'\..*', '.aa.jsonl', fn), 'w', encoding='utf-8')
input_set = set()
type_set = set()

def get_l(types, l):
    anno = int(l[0])
    annos = [types[anno]]
    input = l[2:]
    if input and input[0] == '"':
        input = input[1:]
    if input and input[-1] == '"':
        input = input[:-1]
    return annos, input

def get_j(j):
    annos = [row['value']['choices'][0] for row in j['annotations'][0]['result']]
    input = j['data']['text']
    return annos, input

# ls = open(fn, 'r', encoding='utf-8').read().strip().split('\n')
# ls = ls[1:]
ls = json.loads(open(fn, 'r', encoding='utf-8').read())
for l in tqdm(ls):
    is_in = False
    # annos, input = get_l(types, l)
    annos, input = get_j(l)
    j = {
        'types': types,
        'annos': annos,
        'input': input,
    }
    fh.write(json.dumps(j, ensure_ascii=False) + '\n')
