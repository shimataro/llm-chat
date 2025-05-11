import sys

from llm.llm import LLM


def main(_argv: list[str]) -> int:
    """ メイン関数

    :return: 終了コード
    """
    # モデルの初期化
    llm = LLM()

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
    sys.exit(main(sys.argv))
