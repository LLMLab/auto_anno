import paddle
# paddlenlp==2.6.0rc0
# paddlepaddle-gpu==2.5.0

from paddlenlp.transformers import (
    ChatGLMConfig,
    ChatGLMForConditionalGeneration,
    ChatGLMTokenizer,
)

# 加载模型
#读取原始的chatglm-6b模型
model_name_or_path = 'THUDM/chatglm-6b'
tokenizer = ChatGLMTokenizer.from_pretrained(model_name_or_path)

config = ChatGLMConfig.from_pretrained(model_name_or_path)
paddle.set_default_dtype(config.paddle_dtype)

model = ChatGLMForConditionalGeneration.from_pretrained(
    model_name_or_path,
    tensor_parallel_degree=paddle.distributed.get_world_size(),
    tensor_parallel_rank=0,
    load_state_as_np=True,
    dtype=config.paddle_dtype,
)

model.eval()

# 函数定义，问glm问题（ask_glm）
# 输入参数：初始prompt, 最长输入长度，最长输出长度
def glm_single_QA(model,tokenizer,next_inputs,input_length,output_length):
    # 输入格式转换
    inputs = tokenizer(
        next_inputs,
        return_tensors="np",
        padding=True,
        max_length=input_length,
        truncation=True,
        truncation_side="left",
    )
    input_map = {}
    for key in inputs:
        input_map[key] = paddle.to_tensor(inputs[key])

    # 获取结果
    infer_result = model.generate(
        **input_map,
        decode_strategy="sampling",
        top_k=1,
        # top_p =5,
        max_length=output_length,
        use_cache=True,
        use_fast=True,
        use_fp16_decoding=True,
        repetition_penalty=1,
        # temperature = 0.95,
        temperature = 0.1,
        length_penalty=1,
    )[0]

    # 结果转换
    output = ''
    result = []
    for x in infer_result.tolist():
        res = tokenizer.decode(x, skip_special_tokens=True)
        res = res.strip("\n")
        result.append(res)
        output = output + res
    return output

def chat_chatglm_paddle(prompt, his=[], prompt_his_str='你：{}\n分身：{}'):
    Q_his = '\n'.join([prompt_his_str.format(i[0], i[1]) for i in his])
    if Q_his:
        Q_his += '\n'
    Q_motif = f'{Q_his}${prompt}'
    result=glm_single_QA(model,tokenizer,Q_motif,256,256)
    return result

def en2cn_glm(prompt):
    Q_motif = f'你是一个有百年经验的英汉翻译官，请你翻译以下句子\n{prompt}\n翻译结果为：'
    result=glm_single_QA(model,tokenizer,Q_motif,256,256)
    return result

if __name__ == '__main__':
  content = chat_chatglm_paddle('清华大学地址')
  print(content)
