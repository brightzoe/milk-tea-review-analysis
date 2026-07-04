from pathlib import Path

from .chart_generator import ChartGenerator
from .ml_classifier import SklearnSentimentClassifier
from .problem_analyzer import ProblemAnalyzer
from .report_exporter import ReportExporter
from .review_reader import ReviewReader
from .sentiment_analyzer import SentimentAnalyzer
from .sentiment_lexicon import SentimentLexicon
from .statistics_manager import StatisticsManager
from .suggestion_generator import SuggestionGenerator
from .text_cleaner import TextCleaner


class SystemController:
    def run(self, input_path: str | Path, output_dir: str | Path, verbose: bool = True):
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        charts_dir = output / "charts"
        charts_dir.mkdir(parents=True, exist_ok=True)

        lexicon = SentimentLexicon()
        problem_analyzer = ProblemAnalyzer()
        reviews = ReviewReader().read_csv(input_path)
        brand_product_words = {review.brand for review in reviews} | {review.product for review in reviews}
        vocabulary = (
            lexicon.sentiment_words()
            | set(lexicon.degree_words)
            | lexicon.negation_words
            | problem_analyzer.vocabulary()
            | brand_product_words
            | {"甜度合适", "包装好", "服务好", "速度快", "料足"}
        )

        cleaner = TextCleaner(vocabulary=vocabulary, stopwords_path=Path("data") / "stopwords.txt")
        sentiment_analyzer = SentimentAnalyzer(lexicon)

        for review in reviews:
            review.tokens = cleaner.extract_tokens_for_review(review.content, [review.brand, review.product])
            sentiment_analyzer.analyze(review)
            problem_analyzer.analyze(review)

        ml_classifier = SklearnSentimentClassifier()
        ml_metrics = ml_classifier.evaluate(reviews)
        for review in reviews:
            review.ml_sentiment_label = ml_classifier.predict(review.content)

        summary = StatisticsManager().build_summary(reviews)
        summary.ml_metrics = ml_metrics
        SuggestionGenerator().enrich_summary(summary)

        ChartGenerator(charts_dir).generate_all(summary)

        exporter = ReportExporter()
        exporter.export_csv(reviews, output / "analyzed_reviews.csv")
        exporter.export_markdown(summary, reviews, output / "analysis_report.md")
        ml_classifier.save_evaluation(ml_metrics, output / "ml_evaluation.txt")
        ml_classifier.save_model(output / "sentiment_model.pkl")

        if verbose:
            self._print_console_summary(summary, output)
        return summary

    def _print_console_summary(self, summary, output: Path) -> None:
        print(f"评论总数: {summary.total_count}")
        print("规则模型情感分布:")
        for label in ("正面", "中性", "负面"):
            print(f"  {label}: {summary.sentiment_counts.get(label, 0)}")
        print("主要问题前三名:")
        for category, count in sorted(summary.problem_counts.items(), key=lambda item: item[1], reverse=True)[:3]:
            print(f"  {category}: {count}")
        print("各品牌负面比例:")
        for report in summary.brand_reports:
            ratio = report.negative_count / report.total_count if report.total_count else 0
            print(f"  {report.brand}: {ratio:.1%}")
        print("与人工标签一致率:")
        for name, rate in summary.consistency_rates.items():
            print(f"  {name}: {rate:.2%}")
        print(f"输出文件: {output / 'analyzed_reviews.csv'}")
        print(f"输出报告: {output / 'analysis_report.md'}")
        print(f"模型评估: {output / 'ml_evaluation.txt'}")
        print(f"模型文件: {output / 'sentiment_model.pkl'}")
