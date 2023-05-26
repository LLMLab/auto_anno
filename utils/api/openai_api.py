import openai
import sys
sys.path.append('.')
from local_config import openai_key

if type(openai_key) == list:
    openai_keys = openai_key
else:
    openai_keys = [openai_key]

# Set up your API key
openai.api_key = openai_keys[0]

i = 0

def chat(user):
    global i
    i += 1
    if i >= len(openai_keys):
        i = 0
    openai.api_key = openai_keys[i]
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"{user}"},
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content
    print(content)

    return content

if __name__ == '__main__':
    import flask
    app = flask.Flask(__name__)
    @app.route('/chat', methods=['POST'])
    def chat_api():
        user = flask.request.form.get('user')
        return chat(user)
    app.run(port=5000, host='0.0.0.0')
