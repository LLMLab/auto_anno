import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
import time
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import requests

import websocket
import requests

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    # print("### closed ###")
    pass


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
        return 404, ''
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # print(content, end='')
        if status == 2:
            ws.close()
            return 200, content
    return 0, content


def gen_params(appid, question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": "general",
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": [
                    {"role": "user", "content": question}
                ]
            }
        }
    }
    return data


def main(appid, api_key, api_secret, gpt_url, question):
    outs = []
    state = {'is_close': False}
    cnt = 0
    def _on_message(ws, message):
        is_close, content = on_message(ws, message)
        state['is_close'] = is_close
        outs.append(content)
    def _on_error(ws, error):
        on_error(ws, error)
        state["is_close"] = True
    def _on_close(ws, *args):
        on_close(ws)
        state["is_close"] = True
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=_on_message, on_error=_on_error, on_close=_on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    while cnt < 5*30: # 最多等30秒
        time.sleep(0.2)
        if state['is_close']:
            return ''.join(outs)
    return ''
def chat_xunfei(prompt):
    from ...local_config import config
    xunfei_api = config['xunfei']
    content = main(appid=xunfei_api['appid'],
         api_secret=xunfei_api["api_secret"],
         api_key=xunfei_api["api_key"],
         gpt_url="ws://spark-api.xf-yun.com/v1.1/chat",
         question=prompt)
    return content

def en2cn_xunfei(prompt):
    Q_motif = f'你是一个有百年经验的英汉翻译官，请你翻译以下句子\n{prompt}\n翻译结果为：'
    result=chat_xunfei(Q_motif)
    return result

class EmbeddingReq(object):

    def __init__(self, appid, api_key, api_secret, embedding_url):
        self.APPID = appid
        self.APIKey = api_key
        self.APISecret = api_secret
        self.host = urlparse(embedding_url).netloc
        self.path = urlparse(embedding_url).path
        self.url = embedding_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "POST " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

    def get_Embedding(self, text):
        param_dict = {
            'header': {
                'app_id': self.APPID
            },
            'payload': {
                'text': text
            }
        }
        response = requests.post(url=self.create_url(), json=param_dict)
        result = json.loads(response.content.decode('utf-8'))
        if result['header']['code'] == 0:
            return result['payload']['text']['vector']
        return None

def emb_xunfei(prompt):
    from ...local_config import config
    xunfei_api = config['xunfei']
    embedding_xunfei = EmbeddingReq(
            appid=xunfei_api['appid'],
            api_key=xunfei_api['api_key'],
            api_secret=xunfei_api['api_secret'],
            embedding_url="https://knowledge-retrieval.cn-huabei-1.xf-yun.com/v1/aiui/embedding/query"
        )
    emb = embedding_xunfei.get_Embedding(prompt)
    return emb

"""
    1、配置好python、pip的环境变量
    2、执行 pip install websocket 与 pip3 install websocket-client
    3、去控制台https://console.xfyun.cn/services/cbm获取appid等信息填写即可
"""
if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    print(chat_xunfei("你是谁？你能做什么"))
    print(emb_xunfei("这个问题的向量是什么？"))
