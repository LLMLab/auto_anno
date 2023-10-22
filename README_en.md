# auto_anno

[中文](README.md) | English

An AI-assisted automatic annotation project based on a large model that classifies input text, extracts entities, and translates it into Chinese.

### Basic abilities

### NLP

- Text classification: sentiment classification, news classification, intent recognition, etc.
- Entity extraction: address extraction, character extraction, etc., name type start end
- Text translation: supports batch English-Chinese translation, English data set to Chinese data set
- Clustering: cluster according to vectors, return cluster center point data, and reduce labeling work
- Data generation: Supports generating text data based on categories and expanding data sets

### CV

- Target detection: supports general target detection and has been docked with [whale-anno](https://github.com/datawhalechina/whale-anno) supports visual annotation

## Experience address

https://aistudio.baidu.com/serving/app/6566/

## Support model

OpenAI-api、ChatGLM、erniebot、SparkApi

All the above models are supported. You can use it by filling in the corresponding key or url in local config py.

## Quick to use

### Start locally

```shell
git clone https://github.com/LLMLab/auto_anno.git
cd auto_anno
python app.gradio.py
```

### via pip package

Install the latest auto anno 2 package

```shell
pip install auto_anno_2 -U -i https://pypi.org/simple
```

Call example

```python
import auto_anno_2 as aa2
# The interface uses Wen Xinyiyan by default, and you can get 1 million tokens for free from https://aistudio.baidu.com/usercenter/token
aa2.config['aistudio']['access_token'] = '3c410ce131fe8d246c47e26fdf932cfd44e95aa8'
aa2.cls('今天会下雨么？', ['天气查询', '股票查询', '其他']) # Text Categorization
# ['天气查询']
aa2.ner('茅台今天会涨么？', ['股票名称']) # Entity extraction
# [{'name': '茅台', 'type': '股票名称', 'start': 0, 'end': 2}]
aa2.gen(['天气查询', '股票查询']) # Data generation
# [['明天北京的天气怎么样？', ['天气查询']], ['上海股市大盘走势图今天有什么变化？', ['股票查询']], ['最近一段时间天气是晴朗还是多云？', ['天气查询']], ['美国股市纳斯达克指数现在的行情如何？', ['股票查询']], ['未来一周广州的天气预报已经发布了吗？', ['天气查询']], ['阿里巴巴的股票价格涨了还是跌了？', ['股票查询']], ['明天上海的气温会降到零下五度吗？', ['天气查询']], ['腾讯控股的股票可以买还是应该卖？', ['股票查询']], ['下周武汉的天气预报是否有雨？', ['天气查询']], ['苹果公司的股票收益在过去一年中如何？', ['股票查询']]]

```

## News

2023-09-24 🔥 auto_anno_2 pip package online

2023-09-04 💦 Start training a general classification large model with A100

2023-08-31 💥 Completed the classification and extraction of 984,000 pieces of data in common formats

2023-08-18 🔥 General basic target detection

2023-08-10 🔥 few shots that have been labeled with similar data

...

2023-05-08 ⭐ Project establishment, adding the first line of code, project configuration

## Follow-up plan

* [ ] Open up data whale's open source annotation tool whale anno, used for manual correction of data
* [ ] Training basic large models for nlp and cv related annotation can better reduce repeated annotation of data, improve annotation efficiency, and focus on key data;

  * [X] Collect nearly 1 million public nlp data and convert it into a common format
  * [ ] Training classification and entity extraction models (classification training in progress)
  * [ ] Try training a few shot task
  * [ ] Try to distill it into a 100M small model, suitable for local CPU inference
  * [X] Test effect
* [ ] Seek opportunities to cooperate and develop with more real-life scenarios and explore more possibilities;

## Achievements achieved

2023-08-12 Won the third prize of Baidu 2023 Large Model Application Innovation Challenge Application Track

2023-05-19 Get the best application award for data whale aigc theme chat gpt from entry to application

## Contribution list

|         Responsibilities         |                                     Name                                     |
| :-------------------------------: | :--------------------------------------------------------------------------: |
|      **Group leader**      |                     [马琦钧](https://github.com/Skypow2012)                     |
|          Active learning          |                      [小驰同学](https://github.com/zsc19)                      |
|    Text classification prompt    |                  の男、[Cyfee](https://github.com/Cyfee)、S13D                  |
|     Entity extraction prompt     | [Ken](https://github.com/C0dem0nk3y)、[Furong](https://github.com/momo4826)、log23 |
|         Cluster selection         |   [小驰同学](https://github.com/zsc19)、[马琦钧](https://github.com/Skypow2012)   |
| Text translation, data generation |                     [马琦钧](https://github.com/Skypow2012)                     |
|         Target Detection         |                  の男、[马琦钧](https://github.com/Skypow2012)                  |
|        Document management        |                                  Jun、S13D                                  |
|    ChatGLM, VisualGLM explore    |                                     Mike                                     |
