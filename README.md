# 面向奶茶店消费体验的评论情感分析与服务改进建议系统

本项目是一个轻量级 NLP 应用系统，用于分析奶茶店用户评论，输出情感分类、问题归因、品牌对比、图表和服务改进建议。

## 功能

- 读取 `data/reviews.csv` 评论数据。
- 使用情感词典、否定词、程度副词进行规则情感分析。
- 使用 `TF-IDF + LogisticRegression` 训练 sklearn 情感分类器。
- 识别口味、价格、出餐、服务、包装、配送、产品等问题。
- 生成 CSV、Markdown、图表和机器学习评估结果。

## 运行

```bash
pip install -r requirements.txt
python -m src.main
```

自定义路径：

```bash
python -m src.main --input data/reviews.csv --output output
```

## 测试

```bash
python -m unittest discover tests
```

## 输出

- `output/analyzed_reviews.csv`
- `output/analysis_report.md`
- `output/ml_evaluation.txt`
- `output/charts/sentiment_distribution.png`
- `output/charts/brand_sentiment_compare.png`
- `output/charts/problem_ranking.png`

## 数据说明

数据使用 3 个课程项目样例品牌：`蜜雪茶姬`、`瑞巴克`、`爷爷喜欢茶`。

`data/reviews.csv` 由两部分组成：

- ASAP 公开中文餐馆评论 sample 中抽取的真实餐饮评论片段。
- 人工整理的奶茶消费场景样例，用于覆盖珍珠、小料、甜度、冰量、奶盖、外卖包装等奶茶专属问题。

原始 ASAP sample 文件保存在 `data/external/`，最终分析只使用匿名化后的产品体验字段。
