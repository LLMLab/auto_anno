import openai
import requests

i = 0

def chat_openai(user):
    from ...local_config import config
    openai_key = config['openai']['key']
    if type(openai_key) == list:
        openai_keys = openai_key
    else:
        openai_keys = [openai_key]

    # Set up your API key
    openai.api_key = openai_keys[0]
    global i
    i += 1
    if i >= len(openai_keys):
        i = 0
    openai.api_key = openai_keys[i]
    # openai.api_base = "https://api.openai.com/v1"
    # openai.api_base = "http://47.89.230.109/v1"
    # openai.api_base = "https://api.tekii.cn/v1"
    # openai.api_base = "https://api.aiproxy.io/v1"
    openai.api_base = config['openai'].get('api_base', 'https://api.openai.com/v1')
    model = config['openai'].get('model', 'gpt-3.5-turbo')
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": f"{user}"},
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content

    return content

def emb_openai(text):
    from ...local_config import config
    openai_keys = config['openai']['key']
    global i
    i += 1
    if i >= len(openai_keys):
        i = 0
    openai.api_key = openai_keys[i]
    openai.api_base = config['openai'].get('api_base', 'https://api.openai.com/v1')
    emb_model = config['openai'].get('emb_model', 'text-embedding-3-large')
    # 获取embedding
    text = text.replace("\n", " ")
    j = {"input": text, "model": emb_model}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key
    }
    response = requests.post(openai.api_base + "/embeddings", json=j, headers=headers)
    emb = response.json()['data'][0]['embedding']
    return emb

if __name__ == '__main__':
    # content = chat_openai('你好')
    # print(content)
    emb = emb_openai('你好')
    print(emb)
    # import flask
    # app = flask.Flask(__name__)
    # @app.route('/chat', methods=['POST'])
    # def chat_api():
    #     user = flask.request.form.get('user')
    #     return chat(user)
    # app.run(port=5000, host='0.0.0.0')
