import requests
import json

def en2cn_google(text):
    return trans_google(text, 'en', 'zh-CN')

def trans_google(text, sl, tl):
    temp_url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl={sl}&tl={tl}&dt=t&q={q}'
    url = temp_url.format(q=text, sl=sl, tl=tl)
    result = requests.get(url)
    j = json.loads(result.content)
    try:
        cn = ''.join([i[0] for i in j[0]])
        return cn
    except:
        return ''

if __name__ == '__main__':
    # print(en2cn_google('hello world'))
    print(en2cn_google(''))
