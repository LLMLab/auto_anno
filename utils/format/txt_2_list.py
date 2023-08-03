import re

def txt_2_list(txt):
  split_token = r'[ ,、，;；《》<>\n]'
  rm_token = r'["\'”“‘’。.！!？? 【】\[\]]'
    
  arr = re.split(split_token, txt)
  arr = [re.sub(rm_token, '', item) for item in arr if item != '']
  # 从大到小排序
  arr.sort(key=lambda x: len(x), reverse=True)
  return arr
