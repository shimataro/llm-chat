# チャットアプリケーション
import argparse


def main(argv: list[str] | None = None) -> None:
    """ メイン関数

    :param args: コマンドライン引数
    :return: 終了ステータス
    """
    # コマンドライン引数を解析
    params = Parameters(argv)
    print(f"Model Name: {params.model_name}")
    print(f"Access Token: {params.access_token}")
    print(f"Source Language: {params.language_source}")
    print(f"Target Language: {params.language_target}")
    print()

    # モデルの初期化
    print("Loading model...")
    from libs.llm import LLM
    llm = LLM(
        model_name=params.model_name,
        access_token=params.access_token,
        language_source=params.language_source,
        language_target=params.language_target,
    )

    print()
    print("It's time to talk!")
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


class Parameters:
    """ アプリケーションパラメーター """

    def __init__(self, args: list[str] | None):
        """ 引数を解析

        :param args: コマンドライン引数
        """
        parser = argparse.ArgumentParser(
            description="LLM Chat",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""examples:
  %(prog)s -m microsoft/phi-2
  %(prog)s -m meta-llama/Meta-Llama-3-8B-Instruct -t YOUR_ACCESS_TOKEN
  %(prog)s -m facebook/nllb-200-distilled-600M -S eng_Latn -T jpn_Jpan
"""
        )
        parser.add_argument(
            "-m", "--model-name",
            help="使用するモデル名",
            default="elyza/ELYZA-japanese-Llama-2-7b-instruct",
        )
        parser.add_argument(
            "-t", "--access-token",
            help="Hugging Faceのアクセストークン",
        )
        parser.add_argument(
            "-S", "--language-source",
            metavar="SOURCE_LANGUAGE",
            help="入力言語のコード（Text Generation では無効）",
        )
        parser.add_argument(
            "-T", "--language-target",
            metavar="TARGET_LANGUAGE",
            help="出力言語のコード（Text Generation では無効）",
        )

        # 引数を解析
        ns = parser.parse_args(args=args)
        self.model_name: str = ns.model_name
        self.access_token: str | None = ns.access_token
        self.language_source: str | None = ns.language_source
        self.language_target: str | None = ns.language_target


if __name__ == "__main__":
    main()
