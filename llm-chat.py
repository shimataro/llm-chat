# チャットアプリケーション
import argparse
from dataclasses import dataclass
import sys
from typing import Optional, Sequence

from llm.llm import LLM


@dataclass
class Arguments:
    """ コマンドライン引数 """
    model_name: str
    access_token: Optional[str]


def parse_args(args: Optional[Sequence[str]] = None) -> Arguments:
    """ 引数を解析

    :return: 解析結果
    """
    parser = argparse.ArgumentParser(description="LLM Chat")
    parser.add_argument(
        "--model-name", "-m",
        help="使用するモデル名",
        default="elyza/ELYZA-japanese-Llama-2-7b-instruct",
    )
    parser.add_argument(
        "--access-token", "-t",
        help="Hugging Faceのアクセストークン",
    )

    # 引数を解析＆Argumentsクラスに変換
    ns = parser.parse_args(args=args)
    return Arguments(**vars(ns))


def main(args: Arguments) -> int:
    """ メイン関数

    :param args: 解析済み引数
    :return: 終了ステータス
    """
    # コマンドライン引数を取り出す
    print(f"Model Name: {args.model_name}")
    print(f"Access Token: {args.access_token}")
    print()

    # モデルの初期化
    llm = LLM(args.model_name, args.access_token)

    print("Now, let's talk!")

    # ひたすらチャット
    while True:
        try:
            # 入力プロンプト
            print("> ", end="", flush=True)

            input_text = input().strip()
            if input_text in ("exit", "quit"):
                break

            llm.print_inference_result(input_text)

            # 次の入力プロンプトとの間隔を空ける
            print()

        except EOFError:
            # EOFでも終了
            break

    print("See you!")
    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args()))
