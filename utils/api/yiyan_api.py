import requests

def chat_yiyan(prompt, his=[], prompt_his_str='你：{}\n分身：{}'):
    url = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=24.a8f3e5e3e8664acc427ab6cd44227b08.2592000.1692342888.282335-36387559'
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
