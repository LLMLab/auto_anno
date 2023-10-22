# auto_anno

中文 | [English](README_en.md)

一个基于大模型的将输入文本做文本分类，实体抽取并翻译成中文的AI辅助自动标注项目。

## 基础能力

### NLP

- 文本分类：情感分类、新闻分类、意图识别等
- 实体抽取：地址抽取、人物抽取等，name, type, start~end
- 文本翻译：支持批量英中翻译，英文数据集转中文数据集
- 聚类择优：根据向量聚类，返回聚类中心点数据，减少标注工作
- 数据生成：支持根据类别，生成文本数据，扩充数据集

### CV

- 目标检测：支持通用目标检测，并已对接 [whale-anno](https://github.com/datawhalechina/whale-anno) 支持可视化标注

## 体验地址

https://aistudio.baidu.com/serving/app/6566/

## 支持模型

OpenAI-api、ChatGLM、文心一言-千帆api、讯飞星火-SparkApi

以上模型均已支持，在  local_config.py 中填入对应的 key 或 url 即可使用

## 快速使用

### 本地启动

```shell
git clone https://github.com/LLMLab/auto_anno.git
cd auto_anno
python app.gradio.py
```

### 通过pip包

安装最新 auto_anno_2 包

```shell
pip install auto_anno_2 -U -i https://pypi.org/simple
```

调用示例

```python
import auto_anno_2 as aa2
# 接口默认使用了文心一言，可从 https://aistudio.baidu.com/usercenter/token 免费获取100万token额度
aa2.config['aistudio']['access_token'] = '3c410ce131fe8d246c47e26fdf932cfd44e95aa8'
aa2.cls('今天会下雨么？', ['天气查询', '股票查询', '其他']) # 文本分类
# ['天气查询']
aa2.ner('茅台今天会涨么？', ['股票名称']) # 实体抽取
# [{'name': '茅台', 'type': '股票名称', 'start': 0, 'end': 2}]
aa2.gen(['天气查询', '股票查询']) # 数据生成
# [['明天北京的天气怎么样？', ['天气查询']], ['上海股市大盘走势图今天有什么变化？', ['股票查询']], ['最近一段时间天气是晴朗还是多云？', ['天气查询']], ['美国股市纳斯达克指数现在的行情如何？', ['股票查询']], ['未来一周广州的天气预报已经发布了吗？', ['天气查询']], ['阿里巴巴的股票价格涨了还是跌了？', ['股票查询']], ['明天上海的气温会降到零下五度吗？', ['天气查询']], ['腾讯控股的股票可以买还是应该卖？', ['股票查询']], ['下周武汉的天气预报是否有雨？', ['天气查询']], ['苹果公司的股票收益在过去一年中如何？', ['股票查询']]]

```

## 版本更新

2023-09-24 🔥 auto_anno_2 pip包上线

2023-09-04 💦 开始用A100训练通用分类大模型

2023-08-31 💥 完成整理98.4万条通用格式分类、抽取数据

2023-08-18 🔥 通用的基础目标检测

2023-08-10 🔥 已标注相似数据的 few-shot

...

2023-05-08 ⭐ 项目立项，增加第一行代码，项目配置

## 后续计划

* [ ] 打通 DataWhale 的开源标注工具 whale-anno，用于数据的人工修正
* [ ] 训练用于 NLP、CV 相关标注的基础大模型，能更好地减少数据重复标注、提升标注效率、聚焦重点数据；

  * [X] 收集近100万公开NLP数据，并转为通用格式
  * [ ] 训练分类、实体抽取模型（分类训练中）
  * [ ] 尝试训练 few-shot 任务
  * [ ] 尝试蒸馏成百兆小模型，适用本地CPU推理
  * [X] 测试效果
* [ ] 寻求机会和更多真实场景合作开发，探索更多的可能；

## 已达成就

2023-08-12 获得 百度2023大模型应用创新挑战赛 应用赛道 三等奖

2023-05-19 获得 DataWhale AIGC 主题 ChatGPT 从入门到应用 最佳应用奖

## 贡献名单

|               职责               |                                     名单                                     |
| :-------------------------------: | :--------------------------------------------------------------------------: |
|         **小组长**         |                     [马琦钧](https://github.com/Skypow2012)                     |
|        **主动学习**        |                      [小驰同学](https://github.com/zsc19)                      |
|     **文本分类 Prompt**     |                  の男、[Cyfee](https://github.com/Cyfee)、S13D                  |
|     **实体抽取 Prompt**     | [Ken](https://github.com/C0dem0nk3y)、[Furong](https://github.com/momo4826)、log23 |
|        **聚类择优**        |   [小驰同学](https://github.com/zsc19)、[马琦钧](https://github.com/Skypow2012)   |
|   **文本翻译、数据生成**   |                     [马琦钧](https://github.com/Skypow2012)                     |
|        **目标检测**        |                  の男、[马琦钧](https://github.com/Skypow2012)                  |
|        **文档管理**        |                                  Jun、S13D                                  |
| **ChatGLM、VisualGLM 探索** |                                     Mike                                     |
