from .models import Review
from .sentiment_lexicon import SentimentLexicon


class SentimentAnalyzer:
    def __init__(self, lexicon: SentimentLexicon) -> None:
        self.lexicon = lexicon

    def analyze(self, review: Review) -> Review:
        score = self.calculate_score(review.tokens)
        review.rule_sentiment_score = round(score, 2)
        review.rule_sentiment_label = self.classify(score)
        return review

    def calculate_score(self, tokens: list[str]) -> float:
        score = 0.0
        for index, token in enumerate(tokens):
            base = self.lexicon.get_base_score(token)
            if base == 0:
                continue
            weight = 1.0
            reversed_score = False
            if index > 0:
                previous = tokens[index - 1]
                weight = self.lexicon.get_degree_weight(previous)
                reversed_score = self.lexicon.is_negation(previous)
            if index > 1 and self.lexicon.is_negation(tokens[index - 2]):
                reversed_score = True
            current = base * weight
            if reversed_score:
                current *= -1
            score += current
        return score

    def classify(self, score: float) -> str:
        if score >= 1:
            return "正面"
        if score <= -1:
            return "负面"
        return "中性"
