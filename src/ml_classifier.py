from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .models import Review


class SklearnSentimentClassifier:
    LABELS = ["正面", "中性", "负面"]

    def __init__(self) -> None:
        self.model = Pipeline(
            [
                ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=1000)),
            ]
        )
        self._trained = False

    def train(self, reviews: list[Review]) -> None:
        texts = [review.content for review in reviews]
        labels = [review.label for review in reviews]
        self.model.fit(texts, labels)
        self._trained = True

    def predict(self, text: str) -> str:
        if not self._trained:
            raise RuntimeError("模型尚未训练")
        return str(self.model.predict([text])[0])

    def evaluate(self, reviews: list[Review]) -> dict[str, object]:
        texts = [review.content for review in reviews]
        labels = [review.label for review in reviews]
        stratify = labels if min(labels.count(label) for label in set(labels)) >= 2 else None
        train_x, test_x, train_y, test_y = train_test_split(
            texts,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=stratify,
        )
        self.model.fit(train_x, train_y)
        self._trained = True
        predictions = self.model.predict(test_x)
        precision, recall, f1, _ = precision_recall_fscore_support(
            test_y,
            predictions,
            labels=self.LABELS,
            average="weighted",
            zero_division=0,
        )
        report = classification_report(test_y, predictions, labels=self.LABELS, zero_division=0)
        matrix = confusion_matrix(test_y, predictions, labels=self.LABELS)
        return {
            "accuracy": accuracy_score(test_y, predictions),
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "classification_report": report,
            "confusion_matrix": matrix.tolist(),
            "labels": self.LABELS,
        }

    def save_model(self, output_path: str | Path) -> None:
        """将训练好的 sklearn 模型持久化到文件。"""
        if not self._trained:
            raise RuntimeError("模型尚未训练")
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)

    def load_model(self, model_path: str | Path) -> None:
        """从文件加载已保存的 sklearn 模型。"""
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"模型文件不存在: {path}")
        self.model = joblib.load(path)
        self._trained = True

    def save_evaluation(self, metrics: dict[str, object], output_path: str | Path) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "sklearn 情感分类器评估结果",
            "",
            f"accuracy: {float(metrics['accuracy']):.4f}",
            f"precision: {float(metrics['precision']):.4f}",
            f"recall: {float(metrics['recall']):.4f}",
            f"f1-score: {float(metrics['f1']):.4f}",
            "",
            "classification report:",
            str(metrics["classification_report"]),
            "confusion matrix:",
            str(metrics["confusion_matrix"]),
        ]
        path.write_text("\n".join(lines), encoding="utf-8")
