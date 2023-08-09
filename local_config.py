config = {
    'api': 'yiyan', # openai | chatglm_paddle | chatglm | yiyan | xunfei
    'en2cn': 'yiyan', # google_trans | chatglm_paddle | yiyan | xunfei
    'emb': 'yiyan', # yiyan | xunfei
    'openai': {
        'key': [
            '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',
        ]
    },
    'chatglm': {
        'url': '',
    },
    'yiyan': {
        'access_token': '24.a8f3e5e3e8664acc427ab6cd44227b08.2592000.1692342888.282335-36387559'
    },
    'xunfei': {
        'appid': '',
        'api_secret': '',
        'api_key': ''
    }
}

import time
import random
# chat
if config['api'] == 'openai':
    from utils.api.openai_api import chat_openai as chat
elif config['api'] == 'chatglm_paddle':
    from utils.api.chatglm_paddle import chat_chatglm_paddle as chat
elif config['api'] == 'chatglm':
    from utils.api.chatglm_api import chat_chatglm as chat
elif config['api'] == 'yiyan':
    from utils.api.yiyan_api import chat_yiyan as chat
elif config['api'] == 'xunfei':
    from utils.api.xunfei_api import chat_xunfei as chat
elif config['api'] == 'xunfei':
    from utils.api.xunfei_api import chat_xunfei as chat
else:
    raise Exception('api not supported')

# en2cn
if config['en2cn'] == 'google_trans':
    from utils.api.google_trans import en2cn_google as _en2cn
elif config['en2cn'] == 'chatglm_paddle':
    from utils.api.chatglm_paddle import en2cn_glm as _en2cn
elif config['en2cn'] == 'yiyan':
    from utils.api.yiyan_api import en2cn_yiyan as _en2cn
elif config['en2cn'] == 'xunfei':
    from utils.api.xunfei_api import en2cn_xunfei as _en2cn
else:
    raise Exception('en2cn not supported')
en_cn_cache = {}
def en2cn(txt, use_cache=True):
    if txt.strip() == '':
        return ''
    try_times = 0
    while try_times < 20:
        try_times += 1
        if txt in en_cn_cache and use_cache:
            return en_cn_cache[txt]
        try:
            cn = _en2cn(txt)
            en_cn_cache[txt] = cn
            return cn
        except Exception as e:
            if 'qps limit error' in str(e):
                time.sleep(random.random() * 3)
            else:
                print(txt, e)
                break
    return ''

# emb
if config['emb'] == 'yiyan':
    from utils.api.yiyan_api import emb_yiyan as emb
elif config['emb'] == 'xunfei':
    from utils.api.xunfei_api import emb_xunfei as emb
else:
    raise Exception('emb not supported')
