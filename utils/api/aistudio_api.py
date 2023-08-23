# pip install https://studio-package.bj.bcebos.com/aistudio-0.0.2-py3-none-any.whl
import aistudio
import sys
sys.path.append('.')
from local_config import config
import os
# 配置环境变量
if os.getenv('WEBIDE_USERID') is None:
    os.environ['WEBIDE_USERID'] = config['aistudio']['WEBIDE_USERID']
    os.environ['STUDIO_MODEL_API_URL_PREFIX'] = config['aistudio']['STUDIO_MODEL_API_URL_PREFIX']
    os.environ['STUDIO_MODEL_API_SDK_USER_JWT_TOKEN'] = config['aistudio']['STUDIO_MODEL_API_SDK_USER_JWT_TOKEN']

def chat_aistudio(prompt):
    chat_completion = aistudio.chat.create(
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
    txts = txt
    if type(txt) == str:
        txts = [txt]
    embeddings = aistudio.embed.embedding_v1(
        input=txts,
    )

    vectors = [d['embedding'] for d in embeddings['data']]
    if type(txt) == str:
        return vectors[0]
    return vectors

if __name__ == '__main__':
    print(chat_aistudio("用可爱的语气介绍一下你自己"))
    print(en2cn_aistudio('hello world'))
    print(emb_aistudio(["推荐⼀些美⻝","给我讲个故事"]))
