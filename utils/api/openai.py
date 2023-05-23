import openai
import sys
sys.path.append('.')
from local_config import openai_key

# Set up your API key
openai.api_key = openai_key

def chat(user):
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"{user}"},
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content

    return content
