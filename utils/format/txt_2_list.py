import re

def txt_2_list(txt):
  txt = txt.strip()
  if '\n' in txt:
    arr = txt.split('\n')
  else:
    split_token = r'[ ,、，;；《》<>]'
    arr = re.split(split_token, txt)
  rm_token = r'["\'”“‘’。.！!？? 【】\[\]]'
  arr = [re.sub(rm_token, '', item) for item in arr if item != '']
  # 从大到小排序
  arr.sort(key=lambda x: len(x), reverse=True)
  return arr
