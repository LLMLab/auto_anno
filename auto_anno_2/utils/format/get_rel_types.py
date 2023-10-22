import numpy as np

emb_cache = {}
def cos_sim(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_cache(emb_cache, key):
  if key in emb_cache:
    return emb_cache[key]
  else:
    value = emb(key)
    emb_cache[key] = value
    return value

def get_rel_types(text, types, limit=5):
  t_emb = get_cache(emb_cache, text)
  types_emb = [get_cache(emb_cache, t) for t in types]
  dists = [cos_sim(t_emb, t_emb_) for t_emb_ in types_emb]
  return [t for _, t in sorted(zip(dists, types), reverse=True)][:limit]

if __name__ == '__main__':
  import sys
  sys.path.append('.')
  from auto_anno_2.local_config import emb
  types = get_rel_types('今天天气怎么样', ['天气查询', '股票查询', '证券查询', '娱乐查询', '其他', '十万个为什么'])
  print(types)
else:
  from ...local_config import emb
