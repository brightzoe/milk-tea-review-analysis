import re
from pathlib import Path


class TextCleaner:
    DEFAULT_STOPWORDS = {"的", "了", "啊", "呢", "就是", "这个", "那个", "感觉"}

    def __init__(self, vocabulary: set[str] | None = None, stopwords_path: str | Path | None = None) -> None:
        self.vocabulary = sorted(vocabulary or set(), key=lambda word: (-len(word), word))
        self.stopwords = set(self.DEFAULT_STOPWORDS)
        if stopwords_path:
            path = Path(stopwords_path)
            if path.exists():
                self.stopwords.update(
                    word.strip() for word in path.read_text(encoding="utf-8").splitlines() if word.strip()
                )

    def clean(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[，。！？、；：,.!?;:\-—（）()【】\[\]\"'“”‘’]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def extract_tokens(self, text: str) -> list[str]:
        cleaned = self.clean(text)
        tokens: list[str] = []
        for word in self.vocabulary:
            if word and word in cleaned:
                tokens.append(word)
        if not tokens:
            tokens = [part for part in cleaned.split(" ") if part]
        return self.remove_stopwords(tokens)

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        return [token for token in tokens if token not in self.stopwords]
