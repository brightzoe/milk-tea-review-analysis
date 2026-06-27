class SentimentLexicon:
    def __init__(self) -> None:
        self.positive_words: dict[str, float] = {
            "好喝": 2,
            "清爽": 2,
            "实惠": 2,
            "满意": 2,
            "喜欢": 2,
            "新鲜": 1,
            "方便": 1,
            "划算": 2,
            "香": 1.5,
            "包装好": 1.5,
            "口感好": 2,
            "服务好": 2,
            "速度快": 1.5,
            "甜度合适": 2,
            "料足": 2,
        }
        self.negative_words: dict[str, float] = {
            "难喝": -2,
            "不好喝": -2,
            "太甜": -2,
            "太淡": -1,
            "贵": -2,
            "慢": -1,
            "漏": -2,
            "态度差": -2,
            "不新鲜": -2,
            "排队": -1,
            "等很久": -2,
            "珍珠硬": -1.5,
            "冰太多": -1,
            "料少": -1.5,
            "苦": -1,
            "腻": -1,
            "涨价": -1.5,
            "送错": -2,
            "缺料": -1.5,
            "杯盖不紧": -2,
        }
        self.degree_words: dict[str, float] = {
            "非常": 1.5,
            "特别": 1.5,
            "很": 1.2,
            "有点": 0.8,
            "稍微": 0.8,
            "太": 1.2,
        }
        self.negation_words: set[str] = {"不", "没", "没有", "不是"}

    def get_base_score(self, word: str) -> float:
        if word in self.positive_words:
            return self.positive_words[word]
        return self.negative_words.get(word, 0.0)

    def get_degree_weight(self, word: str) -> float:
        return self.degree_words.get(word, 1.0)

    def is_negation(self, word: str) -> bool:
        return word in self.negation_words

    def sentiment_words(self) -> set[str]:
        return set(self.positive_words) | set(self.negative_words)
