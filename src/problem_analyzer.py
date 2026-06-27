from .models import Review


class ProblemAnalyzer:
    def __init__(self) -> None:
        self.problem_keywords: dict[str, list[str]] = {
            "口味问题": ["难喝", "太甜", "太淡", "腻", "苦", "不好喝", "发腥", "腥味", "异味", "酸酸", "茶味淡", "像喝水"],
            "价格问题": ["贵", "不划算", "涨价", "性价比低"],
            "出餐问题": ["慢", "等很久", "排队", "超时", "出餐慢"],
            "服务问题": ["态度差", "不耐烦", "服务差", "爱答不理", "很凶"],
            "包装问题": ["漏", "洒了", "包装破", "杯子坏", "包装漏", "杯盖不紧", "漏液", "破了"],
            "配送问题": ["配送慢", "送错", "撒漏", "不及时", "超时", "配送超时"],
            "产品问题": ["缺料", "珍珠硬", "珍珠夹生", "夹生", "硬邦邦", "冰太多", "料少", "少加", "没加", "没煮熟"],
        }

    def vocabulary(self) -> set[str]:
        words: set[str] = set()
        for keywords in self.problem_keywords.values():
            words.update(keywords)
        return words

    def analyze(self, review: Review) -> Review:
        if review.rule_sentiment_label == "正面":
            review.problem_categories = []
        else:
            review.problem_categories = self.match_problem_categories(review.content, review.tokens)
        return review

    def match_problem_categories(self, text: str, tokens: list[str] | None = None) -> list[str]:
        token_set = set(tokens or [])
        matched: list[str] = []
        for category, keywords in self.problem_keywords.items():
            if token_set:
                is_matched = any(keyword in token_set for keyword in keywords)
            else:
                is_matched = any(keyword in text for keyword in keywords)
            if is_matched:
                matched.append(category)
        return matched
