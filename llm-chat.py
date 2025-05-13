# チャットアプリケーション
import argparse
from dataclasses import dataclass
from typing import Optional

from libs.llm import LLM


@dataclass
class Parameters:
    """ アプリケーションパラメーター """
    model_name: str
    access_token: Optional[str]
    lang_src: Optional[str]
    lang_tgt: Optional[str]


def parse_args(args: Optional[list[str]]) -> Parameters:
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
    parser.add_argument(
        "--lang-src",
        help="入力言語のコード（Text Generation では無効）",
    )
    parser.add_argument(
        "--lang-tgt",
        help="出力言語のコード（Text Generation では無効）",
    )

    # 引数を解析＆Parametersクラスに変換
    ns = parser.parse_args(args=args)
    return Parameters(**vars(ns))


def main(argv: Optional[list[str]] = None) -> None:
    """ メイン関数

    :param args: 解析済み引数
    :return: 終了ステータス
    """
    # コマンドライン引数を取り出す
    params = parse_args(argv)
    print(f"Model Name: {params.model_name}")
    print(f"Access Token: {params.access_token}")
    print(f"Source Language: {params.lang_src}")
    print(f"Target Language: {params.lang_tgt}")
    print()

    # モデルの初期化
    llm = LLM(
        model_name=params.model_name,
        access_token=params.access_token,
        lang_src=params.lang_src,
        lang_tgt=params.lang_tgt,
    )

    print()
    print("Now, let's talk!")
    print("Type 'exit' to end the conversation.")
    print()

    # ひたすらチャット
    while True:
        try:
            # 入力プロンプト
            print("> ", end="", flush=True)

            input_text = input().strip()
            if input_text == "exit":
                break

            llm.print_inference_result(input_text)

            # 次の入力プロンプトとの間隔を空ける
            print()

        except EOFError:
            # EOFでも終了
            break

    print("See you!")


if __name__ == "__main__":
    main()
