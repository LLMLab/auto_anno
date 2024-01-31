def chat_zhipu(prompt):
    if __name__ == '__main__':
        from auto_anno_2.local_config import config
    else:
        from ...local_config import config
    from zhipuai import ZhipuAI
    api_key = config['zhipu']['api_key']
    client = ZhipuAI(api_key=api_key) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content

if __name__ == '__main__':
    print(chat_zhipu('你能做什么'))
