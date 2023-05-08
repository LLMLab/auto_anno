import openai
import json
import sys
sys.path.append('.')
from local_config import openai_key

# Set up your API key
openai.api_key = openai_key

def extract_named_entities(src_txt, type_arr):
    system = f"你是一个聪明而且有百年经验的命名实体识别（NER）识别器. 你的任务是从一段文本里面提取出相应的实体并且给出标签。你的回答必须用统一的格式。文本用```符号分割。输出采用Json的格式并且标记实体在文本中的位置。实体类型保存在一个数组里{type_arr}"
    user = f"输入|```皮卡丘神奇宝贝```输出|"
    assistant = """[{"name": "皮卡丘", "type": "Person", "start": 0, "end": 3}, {"name": "神奇宝贝", "type": "物种", "start": 4, "end": 8}]"""
    input = f"输入|```{src_txt}```输出|"
    # Call the OpenAI API
    completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"{system}"},
                        {"role": "user", "content": f"{user}"},
                        {"role": "assistant", "content": f"{assistant}"},
                        {"role": "user", "content": f"{input}"}
                    ]
                )

    # Extract the output and parse the JSON array
    content = completion.choices[0].message.content
    print(content)
    j = json.loads(content)
    return j

if __name__ == '__main__':
    # extract_named_entities("```汤姆每天都被杰瑞欺负，皮卡丘越来越想帮忙，竟然还总是被拒绝，心想难道我“皮大仙”这点能力都没有？而且，这货不是被虐狂吧```", ["Person", "物种"])
    extract_named_entities('老百姓心新乡新闻网话说这几天新乡天气还好吧偷笑', ['代称', '行政区'])
    # Tags: PER(人名), LOC(地点名), GPE(行政区名), ORG(机构名)
    # Label   Tag Meaning
    # PER PER.NAM 名字（张三）
    # PER.NOM 代称、类别名（穷人）
    # LOC LOC.NAM 特指名称（紫玉山庄）
    # LOC.NOM 泛称（大峡谷、宾馆）
    # GPE GPE.NAM 行政区的名称（北京）
    # ORG ORG.NAM 特定机构名称（通惠医院）
    # ORG.NOM 泛指名称、统称（文艺公司）
    # 原始标注 老百姓PER.NOM 新乡GPE.NAM
    # gpt-3.5-turbo [{"name": "老百姓", "type": "代称", "start": 0, "end": 4}, {"name": "新乡新闻网", "type": "组织机构", "start": 4, "end": 10}, {"name": "新乡", "type": "行政区", "start": 12, "end": 14}, {"name": "天气", "type": "自然现象", "start": 14, "end": 16}]
    # ERNIE-UIE {"text":"老百姓心新乡新闻网话说这几天新乡天气还好吧偷笑","result":[{"行政区":[{"text":"新乡","start":4,"end":6,"probability":0.589552328738506}]}]}

