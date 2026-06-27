from collections import Counter, defaultdict

from .models import AnalysisSummary, BrandReport, Review


class StatisticsManager:
    LABELS = ("正面", "中性", "负面")

    def build_summary(self, reviews: list[Review]) -> AnalysisSummary:
        sentiment_counts = self.count_sentiment_labels(reviews)
        problem_counts = self.count_problem_categories(reviews)
        keyword_counts = self.count_keywords(reviews)
        label_counts = dict(Counter(review.label for review in reviews))
        brand_reports = self.analyze_by_brand(reviews)
        return AnalysisSummary(
            total_count=len(reviews),
            sentiment_counts=sentiment_counts,
            problem_counts=problem_counts,
            keyword_counts=keyword_counts,
            brand_reports=brand_reports,
            label_counts=label_counts,
        )

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
