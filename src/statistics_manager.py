from collections import Counter, defaultdict

from .models import AnalysisSummary, BrandReport, Review


class StatisticsManager:
    LABELS = ("正面", "中性", "负面")

    def build_summary(self, reviews: list[Review]) -> AnalysisSummary:
        self.assign_rating_labels(reviews)
        sentiment_counts = self.count_sentiment_labels(reviews)
        problem_counts = self.count_problem_categories(reviews)
        keyword_counts = self.count_keywords(reviews)
        label_counts = dict(Counter(review.label for review in reviews))
        consistency_rates = self.calculate_consistency_rates(reviews)
        brand_reports = self.analyze_by_brand(reviews)
        return AnalysisSummary(
            total_count=len(reviews),
            sentiment_counts=sentiment_counts,
            problem_counts=problem_counts,
            keyword_counts=keyword_counts,
            brand_reports=brand_reports,
            label_counts=label_counts,
            consistency_rates=consistency_rates,
        )

    def assign_rating_labels(self, reviews: list[Review]) -> None:
        for review in reviews:
            review.rating_sentiment_label = self.rating_to_label(review.rating)

    def rating_to_label(self, rating: int) -> str:
        if rating >= 4:
            return "正面"
        if rating <= 2:
            return "负面"
        return "中性"

    def calculate_consistency_rates(self, reviews: list[Review]) -> dict[str, float]:
        total = len(reviews)
        if total == 0:
            return {"规则模型": 0.0, "机器学习模型": 0.0, "评分映射": 0.0}
        return {
            "规则模型": self._match_rate(reviews, "rule_sentiment_label"),
            "机器学习模型": self._match_rate(reviews, "ml_sentiment_label"),
            "评分映射": self._match_rate(reviews, "rating_sentiment_label"),
        }

    def _match_rate(self, reviews: list[Review], field_name: str) -> float:
        matched = sum(1 for review in reviews if getattr(review, field_name) == review.label)
        return round(matched / len(reviews), 4)

    def count_sentiment_labels(self, reviews: list[Review]) -> dict[str, int]:
        counts = Counter(review.rule_sentiment_label for review in reviews)
        return {label: counts.get(label, 0) for label in self.LABELS}

    def count_problem_categories(self, reviews: list[Review]) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for review in reviews:
            counts.update(review.problem_categories)
        return dict(counts)

    def count_keywords(self, reviews: list[Review]) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for review in reviews:
            counts.update(review.tokens)
        return dict(counts)

    def analyze_by_brand(self, reviews: list[Review]) -> list[BrandReport]:
        grouped: dict[str, list[Review]] = defaultdict(list)
        for review in reviews:
            grouped[review.brand].append(review)

        reports: list[BrandReport] = []
        for brand in sorted(grouped):
            items = grouped[brand]
            label_counts = Counter(review.rule_sentiment_label for review in items)
            problem_counts: Counter[str] = Counter()
            keyword_counts: Counter[str] = Counter()
            for review in items:
                problem_counts.update(review.problem_categories)
                keyword_counts.update(review.tokens)
            avg_score = sum(review.rule_sentiment_score for review in items) / len(items)
            reports.append(
                BrandReport(
                    brand=brand,
                    total_count=len(items),
                    positive_count=label_counts.get("正面", 0),
                    neutral_count=label_counts.get("中性", 0),
                    negative_count=label_counts.get("负面", 0),
                    average_score=round(avg_score, 2),
                    top_problems=problem_counts.most_common(3),
                    top_keywords=keyword_counts.most_common(8),
                )
            )
        return reports
