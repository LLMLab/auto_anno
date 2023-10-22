# 一个分类项目

可以挑选出置信度低的样本，重新标注。

## 环境

```shell
# We highly suggest you using Anaconda to manage your python environment.
conda create -y --force -n Text-Classification python=3.6 pip
conda activate Text-Classification
pip install -r requirement.txt
```

## 数据准备

**训练集；测试集；标签**

data/train.csv; data/test.csv; label

## 预训练模型

**下载roberta预训练模型** [从哈工大官方github下载，点这里](https://github.com/ymcui/Chinese-BERT-wwm#中文模型下载)，下载RBT3,Chinese 版本，修改以下代码

```
config_path = 'D:\download\Data\Bert Model\chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = 'D:\download\Data\Bert Model\chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = 'D:\download\Data\Bert Model\chinese_L-12_H-768_A-12/vocab.txt'
```



## How to run it

```shell
# 训练
python train.py

# 预测返回低置信度样本
python predict.py
```

模型对data/test_data.csv的数据重新打分并排序得到output_sort.csv，取低置信度的20%为output_low_confidence.csv，对此部分应检查是否标注错误。



## 参考

https://github.com/DeqianBai/KBQA-study