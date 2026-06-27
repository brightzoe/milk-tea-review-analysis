import csv
from pathlib import Path

from .models import Review


class ReviewReader:
    REQUIRED_FIELDS = {
        "review_id",
        "date",
        "brand",
        "product",
        "channel",
        "content",
        "rating",
        "label",
    }
    VALID_LABELS = {"正面", "中性", "负面"}

    def read_csv(self, file_path: str | Path) -> list[Review]:
        path = Path(file_path)
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError("CSV 文件缺少表头")
            missing = self.REQUIRED_FIELDS - set(reader.fieldnames)
            if missing:
                raise ValueError(f"CSV 缺少字段: {', '.join(sorted(missing))}")
            return [self.create_review(row, index) for index, row in enumerate(reader, start=2)]

    def create_review(self, row: dict[str, str], row_number: int = 0) -> Review:
        self.validate_row(row, row_number)
        return Review(
            review_id=row["review_id"].strip(),
            date=row["date"].strip(),
            brand=row["brand"].strip(),
            product=row["product"].strip(),
            channel=row["channel"].strip(),
            content=row["content"].strip(),
            rating=int(row["rating"]),
            label=row["label"].strip(),
        )

    def validate_row(self, row: dict[str, str], row_number: int = 0) -> None:
        prefix = f"第 {row_number} 行" if row_number else "当前行"
        for field in self.REQUIRED_FIELDS:
            if field not in row or row[field] is None or not str(row[field]).strip():
                raise ValueError(f"{prefix} 缺少有效字段: {field}")
        try:
            rating = int(row["rating"])
        except ValueError as exc:
            raise ValueError(f"{prefix} rating 必须是整数") from exc
        if rating < 1 or rating > 5:
            raise ValueError(f"{prefix} rating 必须在 1 到 5 之间")
        if row["label"].strip() not in self.VALID_LABELS:
            raise ValueError(f"{prefix} label 必须是 正面/中性/负面")
