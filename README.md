# auto_anno

一个基于大模型的将输入文本做文本分类，实体抽取并翻译成中文的AI辅助自动标注项目。

## 基础能力

- 文本分类：情感分类、新闻分类、意图识别等
- 实体抽取：地址抽取、人物抽取等，name, type, start~end

## 体验地址

https://aistudio.baidu.com/aistudio/projectdetail/6542456

## 支持模型

OpenAI-api、ChatGLM、文心一言-千帆api、讯飞星火-SparkApi

以上模型均已支持，在  local_config.py 中填入对应的 key 或 url 即可使用

## 快速使用

```shell
git clone https://github.com/LLMLab/auto_anno.git
cd auto_anno
python app.gradio.py
```

## 贡献名单

|           职责           |                                     名单                                     |
| :-----------------------: | :--------------------------------------------------------------------------: |
|     **小组长**     |                     [马琦钧](https://github.com/Skypow2012)                     |
|    **主动学习**    |                      [小驰同学](https://github.com/zsc19)                      |
| **文本分类 Prompt** |                  の男、[Cyfee](https://github.com/Cyfee)、S13D                  |
| **实体抽取 Prompt** | [Ken](https://github.com/C0dem0nk3y)、[Furong](https://github.com/momo4826)、log23 |
|    **文档管理**    |                                     Jun                                     |
|  **ChatGLM 探索**  |                                     Mike                                     |
