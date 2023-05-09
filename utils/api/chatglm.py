import requests

# 页面地址 https://fd7fa865d3f27cda69.gradio.live/
# 指定请求的数据
data = {'prompt': '清华大学地址'}
# 发送POST请求到API
response = requests.post('http://region-9.seetacloud.com:51661/', json=data)
# 获取预测结果
result = response.json()
print(result)
