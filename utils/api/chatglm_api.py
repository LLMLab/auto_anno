import requests
import sys
sys.path.append('.')
from local_config import config

# 页面地址 https://fd7fa865d3f27cda69.gradio.live/
# 指定请求的数据
def chat_chatglm(prompt):
  # 发送POST请求到API
  url = config['chatglm']['url']
  data = {'prompt': prompt}
  response = requests.post(url, json=data)
  # 获取预测结果
  result = response.json()
  print(result)

if __name__ == '__main__':
  content = chat_chatglm('清华大学地址')
  print(content)
