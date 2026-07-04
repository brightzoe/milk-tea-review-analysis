import csv
from pathlib import Path

from .models import AnalysisSummary, Review


class ReportExporter:
    def export_csv(self, reviews: list[Review], output_path: str | Path) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = [
            "review_id",
            "date",
            "brand",
            "product",
            "channel",
            "content",
            "rating",
            "rating_sentiment_label",
            "label",
            "tokens",
            "rule_sentiment_score",
            "rule_sentiment_label",
            "ml_sentiment_label",
            "problem_categories",
        ]
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for review in reviews:
                writer.writerow(
                    {
                        "review_id": review.review_id,
                        "date": review.date,
                        "brand": review.brand,
                        "product": review.product,
                        "channel": review.channel,
                        "content": review.content,
                        "rating": review.rating,
                        "rating_sentiment_label": review.rating_sentiment_label,
                        "label": review.label,
                        "tokens": " ".join(review.tokens),
                        "rule_sentiment_score": review.rule_sentiment_score,
                        "rule_sentiment_label": review.rule_sentiment_label,
                        "ml_sentiment_label": review.ml_sentiment_label,
                        "problem_categories": "、".join(review.problem_categories),
                    }
                )

    def export_markdown(self, summary: AnalysisSummary, reviews: list[Review], output_path: str | Path) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines: list[str] = [
            "# 奶茶店评论情感分析与服务改进建议报告",
            "",
            "## 一、数据概况",
            "",
            f"- 评论总数：{summary.total_count}",
            "- 品牌名称为课程项目样例品牌：蜜雪茶姬、瑞巴克、爷爷喜欢茶。",
            "- 数据由 ASAP 公开中文餐馆评论 sample 和人工整理的奶茶消费场景样例组成，已去除个人信息。",
            "",
            "### 人工标注情感分布",
            "",
            "| 情感类别 | 数量 |",
            "|---|---:|",
        ]
        for label in ("正面", "中性", "负面"):
            lines.append(f"| {label} | {summary.label_counts.get(label, 0)} |")

        lines.extend(
            [
                "",
                "### 情感标签说明",
                "",
                "- `label` 为人工标注情感类别，用于监督学习训练和评估。",
                "- `rating_sentiment_label` 由评分映射得到：4-5 分为正面，3 分为中性，1-2 分为负面。",
                "- 系统最终分析不直接使用 rating 判断情感，而是根据评论文本进行规则分析和机器学习预测，再与人工标签、评分映射结果进行对比。",
                "",
                "### 与人工标签一致率",
                "",
                "| 对比对象 | 一致率 |",
                "|---|---:|",
            ]
        )
        for name in ("规则模型", "机器学习模型", "评分映射"):
            rate = summary.consistency_rates.get(name, 0.0)
            lines.append(f"| {name} | {rate:.2%} |")

        lines.extend(
            [
                "",
                "## 二、规则模型分析结果",
                "",
                "| 情感类别 | 数量 |",
                "|---|---:|",
            ]
        )
        for label in ("正面", "中性", "负面"):
            lines.append(f"| {label} | {summary.sentiment_counts.get(label, 0)} |")

        lines.extend(["", "### 品牌对比", "", "| 品牌 | 评论数 | 正面 | 中性 | 负面 | 平均规则得分 |", "|---|---:|---:|---:|---:|---:|"])
        for report in summary.brand_reports:
            lines.append(
                f"| {report.brand} | {report.total_count} | {report.positive_count} | "
                f"{report.neutral_count} | {report.negative_count} | {report.average_score:.2f} |"
            )

        lines.extend(["", "### 主要问题排行", "", "| 问题类别 | 出现次数 |", "|---|---:|"])
        for category, count in sorted(summary.problem_counts.items(), key=lambda item: item[1], reverse=True):
            lines.append(f"| {category} | {count} |")

        lines.extend(["", "### 高频关键词 Top 15", "", "| 关键词 | 出现次数 |", "|---|---:|"])
        for keyword, count in sorted(summary.keyword_counts.items(), key=lambda item: item[1], reverse=True)[:15]:
            lines.append(f"| {keyword} | {count} |")

        metrics = summary.ml_metrics
        lines.extend(
            [
                "",
                "## 三、sklearn 机器学习模型结果",
                "",
                f"- accuracy：{float(metrics.get('accuracy', 0.0)):.4f}",
                f"- precision：{float(metrics.get('precision', 0.0)):.4f}",
                f"- recall：{float(metrics.get('recall', 0.0)):.4f}",
                f"- f1-score：{float(metrics.get('f1', 0.0)):.4f}",
                "",
                "```text",
                str(metrics.get("classification_report", "")).strip(),
                "```",
                "",
                "## 四、图表输出",
                "",
                "- 总体情感分布：`charts/sentiment_distribution.png`",
                "- 品牌情感对比：`charts/brand_sentiment_compare.png`",
                "- 负面问题排行：`charts/problem_ranking.png`",
                "",
                "## 五、各品牌改进建议",
                "",
            ]
        )
        for report in summary.brand_reports:
            lines.append(f"### {report.brand}")
            for suggestion in report.suggestions:
                lines.append(f"- {suggestion}")
            lines.append("")

        negative_examples = [review for review in reviews if review.rule_sentiment_label == "负面"][:5]
        lines.extend(["## 六、典型负面评论样例", "", "| 品牌 | 产品 | 评论 | 问题归因 |", "|---|---|---|---|"])
        for review in negative_examples:
            lines.append(
                f"| {review.brand} | {review.product} | {review.content} | {'、'.join(review.problem_categories)} |"
            )

        lines.extend(
            [
                "",
                "## 七、方法对比与不足",
                "",
                "- 规则模型优点是可解释，能说明具体扣分词和问题类别，适合生成经营建议。",
                "- sklearn 模型能从标注数据中学习文本模式，适合展示监督学习分类流程。",
                "- 当前数据规模仍有限，分类效果受样本覆盖范围和人工标注质量影响。",
            ]
        )
        path.write_text("\n".join(lines), encoding="utf-8")
