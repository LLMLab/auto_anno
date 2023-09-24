config = {
    'api': 'aistudio', # openai | chatglm_paddle | chatglm | yiyan | xunfei | aistudio
    'en2cn': 'aistudio', # google_trans | chatglm_paddle | yiyan | xunfei | aistudio
    'emb': 'aistudio', # yiyan | xunfei | aistudio
    'log': {
        'silent': True
    },
    'openai': {
        'key': [
            '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',
        ]
    },
    'chatglm': {
        'url': '',
    },
    'yiyan': {
        'access_token': '24.f98fd9187ebb6571194d29108b77a3a9.2592000.1695394520.282335-36387559'
    },
    'xunfei': {
        'appid': '',
        'api_secret': '',
        'api_key': ''
    },
    'aistudio': {
        'access_token': '3c410ce131fe8d246c47e26fdf932cfd44e95aa8'
    }
}

import time
import random

def try_more(fn, *args):
    return fn(*args) # 请求单次
    try_times = 0
    while try_times < 20:
        try:
            try_times += 1
            content = fn(*args)
            return content
        except Exception as e:
            if 'qps limit error' in str(e) or 'rate limit' in str(e):
                time.sleep(random.random() * 3)
            else:
                time.sleep(random.random() * 1)
                print(fn, *args, e)
    return ''

# chat
def chat(prompt):
    if config['api'] == 'openai':
        from .utils.api.openai_api import chat_openai as _chat
    elif config['api'] == 'chatglm_paddle':
        from .utils.api.chatglm_paddle import chat_chatglm_paddle as _chat
    elif config['api'] == 'chatglm':
        from .utils.api.chatglm_api import chat_chatglm as _chat
    elif config['api'] == 'yiyan':
        from .utils.api.yiyan_api import chat_yiyan as _chat
    elif config['api'] == 'xunfei':
        from .utils.api.xunfei_api import chat_xunfei as _chat
    elif config['api'] == 'xunfei':
        from .utils.api.xunfei_api import chat_xunfei as _chat
    elif config['api'] == 'aistudio':
        from .utils.api.aistudio_api import chat_aistudio as _chat
    else:
        raise Exception('api not supported')
    return try_more(_chat, prompt)

# en2cn
en_cn_cache = {}
def en2cn(txt, use_cache=True):
    
    if config['en2cn'] == 'google_trans':
        from .utils.api.google_trans import en2cn_google as _en2cn
    elif config['en2cn'] == 'chatglm_paddle':
        from .utils.api.chatglm_paddle import en2cn_glm as _en2cn
    elif config['en2cn'] == 'yiyan':
        from .utils.api.yiyan_api import en2cn_yiyan as _en2cn
    elif config['en2cn'] == 'xunfei':
        from .utils.api.xunfei_api import en2cn_xunfei as _en2cn
    elif config['en2cn'] == 'aistudio':
        from .utils.api.aistudio_api import en2cn_aistudio as _en2cn
    else:
        raise Exception('en2cn not supported')
    if txt.strip() == '':
        return ''
    if txt in en_cn_cache and use_cache:
        return en_cn_cache[txt]
    cn = try_more(_en2cn, txt)
    en_cn_cache[txt] = cn
    return cn

# emb
def emb(txt):
    if config['emb'] == 'yiyan':
        from .utils.api.yiyan_api import emb_yiyan as _emb
    elif config['emb'] == 'xunfei':
        from .utils.api.xunfei_api import emb_xunfei as _emb
    elif config['emb'] == 'aistudio':
        from .utils.api.aistudio_api import emb_aistudio as _emb
    else:
        raise Exception('emb not supported')
    return try_more(_emb, txt)
