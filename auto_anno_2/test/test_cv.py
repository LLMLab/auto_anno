import requests
import base64

def test_cv():
    # 读取图片
    image = open('imgOut/standard.bmp', 'rb').read()
    # 转为base64
    image = base64.b64encode(image).decode('utf-8')
    # 发送请求
    r = requests.post('http://127.0.0.1:5000/detect', json={'image': image})
    # 打印结果
    print(r.json())

if __name__ == '__main__':
    test_cv()
