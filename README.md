# 面向奶茶店消费体验的评论情感分析与服务改进建议系统

本项目是一个轻量级 NLP 应用系统，用于分析奶茶店用户评论，输出情感分类、问题归因、品牌对比、图表和服务改进建议。

## 功能

- 读取 `data/reviews.csv` 评论数据。
- 使用情感词典、否定词、程度副词进行规则情感分析。
- 使用 `TF-IDF + LogisticRegression` 训练 sklearn 情感分类器。
- 识别口味、价格、出餐、服务、包装、配送、产品等问题。
- 将评分映射标签、规则模型标签、机器学习标签与人工标签进行一致率对比。
- 生成 CSV、Markdown、图表和机器学习评估结果。

## 运行

```bash
pip install -r requirements.txt
python -m src.main
# 或直接运行
python src/main.py
```

自定义路径：

```bash
python -m src.main --input data/reviews.csv --output output
```

## 测试

```bash
python -m unittest discover tests
```

当前测试结果：

```text
Ran 24 tests
OK
```

## 输出

- `output/analyzed_reviews.csv`
- `output/analysis_report.md`
- `output/ml_evaluation.txt`
- `output/sentiment_model.pkl`
- `output/charts/sentiment_distribution.png`
- `output/charts/brand_sentiment_compare.png`
- `output/charts/problem_ranking.png`

## 数据说明

数据使用 3 个课程项目样例品牌：`蜜雪茶姬`、`瑞巴克`、`爷爷喜欢茶`。

`data/reviews.csv` 由两部分组成：

- ASAP 公开中文餐馆评论 sample 中经过饮品场景过滤后抽取的真实奶茶/饮品评论片段。
- 人工扩写的奶茶消费场景样例，用于覆盖珍珠、小料、甜度、冰量、奶盖、外卖包装等奶茶专属问题。

原始 ASAP sample 文件保存在 `data/external/`，最终分析只使用匿名化后的产品体验字段。

## 目录结构

```text
src/       系统核心代码
data/      评论数据、停用词和外部样例数据
tests/     单元测试
docs/      需求、设计、测试、用户手册和实验报告
output/    程序运行后的分析结果和图表
scripts/   样例数据构建脚本
```

## 项目仓库

GitHub 地址：https://github.com/brightzoe/milk-tea-review-analysis.git

## 提交说明

- `plan/` 目录为实验整理过程中的提示材料，不作为正式作业内容提交。
- 正式提交建议包含 `src/`、`data/`、`tests/`、`docs/`、`scripts/`、`README.md`、`requirements.txt` 以及必要的 `output/` 运行结果。
