config = {
    'api': 'openai', # openai | chatglm_paddle | chatglm | yiyan | xunfei
    'openai': {
        'key': [
            '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',
        ]
    },
    'chatglm': {
        'url': '',
    },
    'yiyan': {
        'access_token': ''
    },
    'xunfei': {
        'appid': '',
        'api_secret': '',
        'api_key': ''
    }
}
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
