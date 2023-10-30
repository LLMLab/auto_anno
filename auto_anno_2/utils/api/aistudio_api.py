# pip install https://studio-package.bj.bcebos.com/aistudio-0.0.2-py3-none-any.whl
import erniebot
erniebot.api_type = 'aistudio'

def chat_aistudio(prompt):
    if __name__ == '__main__':
        from auto_anno_2.local_config import config
    else:
        from ...local_config import config
    erniebot.access_token = config['aistudio']['access_token']
    chat_completion = erniebot.ChatCompletion.create(
        model = 'ernie-bot',
        # model = 'ernie-bot-4',
        messages=[{
            "role" : "user" ,
            "content" : prompt
        }]
    )
    content = chat_completion.result
    # print('prompt', prompt)
    # print('content', content)
    return content

def en2cn_aistudio(prompt):
    Q_motif = f'你是一个有百年经验的英汉翻译官，请你翻译以下句子\n{prompt}\n翻译结果为：'
    result=chat_aistudio(Q_motif)
    return result

def emb_aistudio(txt):
    if __name__ == '__main__':
        from auto_anno_2.local_config import config
    else:
        from ...local_config import config
    erniebot.access_token = config['aistudio']['access_token']
    txts = txt
    if type(txt) == str:
        txts = [txt]
    # embeddings max tokens per batch size is 384
    txts = [txt[:384] for txt in txts]
    embeddings = erniebot.Embedding.create(
        model='ernie-text-embedding',
        input=txts,
    )
    vectors = [d['embedding'] for d in embeddings['data']]
    import time
    time.sleep(1)
    if type(txt) == str:
        return vectors[0]
    return vectors

if __name__ == '__main__':
    import sys
    sys.path.append('.')
    print(chat_aistudio("用可爱的语气介绍一下你自己"))
    print(en2cn_aistudio('hello world'))
    print(emb_aistudio(["推荐⼀些美⻝","给我讲个故事"]))
