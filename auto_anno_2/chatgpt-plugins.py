import json
from flask import Flask, request, send_file, make_response
from utils.anno.cls.text_classification import text_classification
from utils.anno.ner.entity_extract import extract_named_entities
import time

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
# import quart_cors
# app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
# app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://yiyan.baidu.com")
# 因为通过 nginx 走 https 转发，所以不需要设置 CORS，/etc/nginx/nginx.conf 配置如下
# add_header 'Access-Control-Allow-Origin' *;
# location / {
#         proxy_pass http://127.0.0.1:5003;
# }
app = Flask(__name__)

def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/classification/", methods=['POST'])
def classification():
    text = request.json.get('text', '')
    types = request.json.get('types', '')
    time.sleep(3)
    return make_json_response({'message': '123'}, 200)
    result = text_classification(text, types)
    print('result', result)


@app.route("/entityextract/", methods=['POST'])
def entityextract():
    text = request.json.get('text', '')
    types = request.json.get('types', '')
    result = extract_named_entities(text, types)
    return make_json_response({'message': result}, 200)


@app.route("/logo.png")
async def plugin_logo():
    """
        注册用的：返回插件的logo，要求48 x 48大小的png文件.
        注意：API路由是固定的，事先约定的。
    """
    return send_file('logo.png', mimetype='image/png')


@app.route("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """
        注册用的：返回插件的描述文件，描述了插件是什么等信息。
        注意：API路由是固定的，事先约定的。
    """
    host = request.host_url
    with open(".well-known/ai-plugin.json", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST", host)
        return text, 200, {"Content-Type": "application/json"}


@app.route("/.well-known/openapi.yaml")
async def openapi_spec():
    """
        注册用的：返回插件所依赖的插件服务的API接口描述，参照openapi规范编写。
        注意：API路由是固定的，事先约定的。
    """
    with open(".well-known/openapi.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
