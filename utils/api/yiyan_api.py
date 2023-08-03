import requests
import sys
sys.path.append('.')
from local_config import config

def chat_yiyan(prompt, his=[], prompt_his_str='你：{}\n分身：{}'):
    access_token = config['yiyan']['access_token']
    url = f'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}'
    result = requests.post(url, json={
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })
    return result.json()['result']

def en2cn_yiyan(prompt):
    Q_motif = f'你是一个有百年经验的英汉翻译官，请你翻译以下句子\n{prompt}\n翻译结果为：'
    result=chat_yiyan(Q_motif)
    return result

def emb_yiyan(prompts):
    if str(type(prompts)) == "<class 'str'>":
        prompts = [prompts]
    # curl 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[API Key]&client_secret=[Secret Key]'
    access_token = config['yiyan']['access_token']
    url = f'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token={access_token}'
    result = requests.post(url, json={
        "input": prompts
    })
    return [d['embedding'] for d in result.json()['data']]

if __name__ == '__main__':
    print(chat_yiyan('你能做什么'))
    print(en2cn_yiyan('hello world'))
    print(emb_yiyan(['hello world']))
