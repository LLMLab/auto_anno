import openai

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
    openai.api_base = "https://api.aiproxy.io/v1"
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": f"{user}"},
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content

    return content

if __name__ == '__main__':
    content = chat_openai('123')
    print(content)
    # import flask
    # app = flask.Flask(__name__)
    # @app.route('/chat', methods=['POST'])
    # def chat_api():
    #     user = flask.request.form.get('user')
    #     return chat(user)
    # app.run(port=5000, host='0.0.0.0')
