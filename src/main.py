import argparse

from .controller import SystemController


def main() -> None:
    parser = argparse.ArgumentParser(description="奶茶店评论情感分析与服务改进建议系统")
    parser.add_argument("--input", default="data/reviews.csv", help="输入 CSV 文件路径")
    parser.add_argument("--output", default="output", help="输出目录")
    args = parser.parse_args()
    SystemController().run(args.input, args.output)


if __name__ == "__main__":
    main()
