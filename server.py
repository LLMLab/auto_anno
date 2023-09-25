from utils.anno.cv.traditional import traditional_detect
from utils.anno.cv.openai_clip import cv_cls_openai
from PIL import Image
import flask
from flask import request
import flask_cors
import cv2
import numpy as np
import base64

app = flask.Flask(__name__)
# 允许跨域访问
flask_cors.CORS(app, supports_credentials=True)

@app.route('/detect', methods=['POST'])
def detect():
    data = {'errCode': 0}
    if flask.request.method == 'POST':
        # base64图片，json格式
        if flask.request.json.get('image'):
            image = flask.request.json['image']
            # base64转为cv2格式
            image = cv2.imdecode(np.fromstring(base64.b64decode(image), np.uint8), cv2.IMREAD_COLOR)
            # 转为cv2单通道格式
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = image.shape

            result = traditional_detect(image)
            data['errCode'] = 0
            data['info'] = {
                'rect_angles': result.rect_angles,
                'contours': result.contours,
                'width': width,
                'height': height
            }
    return flask.jsonify(data)


@app.route('/cv_cls', methods=['POST'])
def cv_cls():
    data = {'errCode': 0}
    if flask.request.method == 'POST':
        # base64图片，json格式
        if flask.request.json.get('image'):
            image = flask.request.json['image']
            types = flask.request.json['types']
            # base64转为cv2格式
            image = cv2.imdecode(np.fromstring(base64.b64decode(image), np.uint8), cv2.IMREAD_COLOR)
            # 转为cv2单通道格式
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = image.shape
            # cv2转Image
            image = Image.fromarray(image)

            result = cv_cls_openai(image, types)
            data['errCode'] = 0
            data['info'] = {
                'result': result,
                'width': width,
                'height': height
            }
    return flask.jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
