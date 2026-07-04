from dataclasses import dataclass, field


@dataclass
class Review:
    review_id: str
    date: str
    brand: str
    product: str
    channel: str
    content: str
    rating: int
    label: str
    tokens: list[str] = field(default_factory=list)
    rating_sentiment_label: str = ""
    rule_sentiment_score: float = 0.0
    rule_sentiment_label: str = ""
    ml_sentiment_label: str = ""
    problem_categories: list[str] = field(default_factory=list)


@dataclass
class BrandReport:
    brand: str
    total_count: int
    positive_count: int
    neutral_count: int
    negative_count: int
    average_score: float
    top_problems: list[tuple[str, int]]
    top_keywords: list[tuple[str, int]]
    suggestions: list[str] = field(default_factory=list)


@dataclass
class AnalysisSummary:
    total_count: int
    sentiment_counts: dict[str, int]
    problem_counts: dict[str, int]
    keyword_counts: dict[str, int]
    brand_reports: list[BrandReport]
    label_counts: dict[str, int] = field(default_factory=dict)
    consistency_rates: dict[str, float] = field(default_factory=dict)
    ml_metrics: dict[str, object] = field(default_factory=dict)
