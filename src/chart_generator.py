from pathlib import Path

from .models import AnalysisSummary


class ChartGenerator:
    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self, summary: AnalysisSummary) -> list[Path]:
        paths: list[Path] = []
        for generator in (
            self.generate_sentiment_distribution,
            self.generate_brand_sentiment_compare,
            self.generate_problem_ranking,
        ):
            try:
                paths.append(generator(summary))
            except Exception as exc:  # pragma: no cover - defensive display fallback
                print(f"图表生成失败: {exc}")
        return paths

    def _prepare_pyplot(self):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False
        return plt

    def generate_sentiment_distribution(self, summary: AnalysisSummary) -> Path:
        plt = self._prepare_pyplot()
        labels = ["正面", "中性", "负面"]
        values = [summary.sentiment_counts.get(label, 0) for label in labels]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(labels, values, color=["#4caf50", "#90a4ae", "#ef5350"])
        ax.set_title("总体情感分布")
        ax.set_xlabel("情感类别")
        ax.set_ylabel("评论数量")
        fig.tight_layout()
        path = self.output_dir / "sentiment_distribution.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def generate_brand_sentiment_compare(self, summary: AnalysisSummary) -> Path:
        plt = self._prepare_pyplot()
        brands = [report.brand for report in summary.brand_reports]
        positive = [report.positive_count for report in summary.brand_reports]
        neutral = [report.neutral_count for report in summary.brand_reports]
        negative = [report.negative_count for report in summary.brand_reports]
        x_positions = range(len(brands))
        width = 0.25
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar([x - width for x in x_positions], positive, width, label="正面", color="#4caf50")
        ax.bar(list(x_positions), neutral, width, label="中性", color="#90a4ae")
        ax.bar([x + width for x in x_positions], negative, width, label="负面", color="#ef5350")
        ax.set_title("品牌情感对比")
        ax.set_xlabel("品牌")
        ax.set_ylabel("评论数量")
        ax.set_xticks(list(x_positions))
        ax.set_xticklabels(brands)
        ax.legend()
        fig.tight_layout()
        path = self.output_dir / "brand_sentiment_compare.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def generate_problem_ranking(self, summary: AnalysisSummary) -> Path:
        plt = self._prepare_pyplot()
        items = sorted(summary.problem_counts.items(), key=lambda item: item[1], reverse=True)[:7]
        labels = [item[0] for item in items] or ["无明显问题"]
        values = [item[1] for item in items] or [0]
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.barh(labels, values, color="#ffb74d")
        ax.invert_yaxis()
        ax.set_title("负面问题类别排行")
        ax.set_xlabel("出现次数")
        fig.tight_layout()
        path = self.output_dir / "problem_ranking.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path
