import argparse
import sys
from pathlib import Path

# 同时支持 `python -m src.main` 和 `python src/main.py` 两种启动方式
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.controller import SystemController


def main() -> None:
    parser = argparse.ArgumentParser(description="奶茶店评论情感分析与服务改进建议系统")
    parser.add_argument("--input", default="data/reviews.csv", help="输入 CSV 文件路径")
    parser.add_argument("--output", default="output", help="输出目录")
    args = parser.parse_args()
    SystemController().run(args.input, args.output)


if __name__ == "__main__":
    main()
