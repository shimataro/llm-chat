# LLM-chat

いろんなLLMでチャット！

## コード例

[llm-chat.py](./llm-chat.py)参照

## コード例の動かし方

```bash
$ pipenv shell
(llm-chat) $ pipenv sync
(llm-chat) $ python llm-chat.py
```

必要なモデル等がロードされた後 `>` が表示されるので、何か話しかけてください。
出力にプロンプトが表示されることがありますが、とりあえず気にしないでください。生成されたプロンプトの確認のためにあえて残しています。

```text
Now, let's talk!
> ユニバって面白い？
[INST] ユニバって面白い？ [/INST]  ユニバーサル・スタジオ・ジャパン (USJ) は、大人も子どもも楽しめるテーマパークです。
USJの魅力は、映画やテレビ番組などの人気キャラクターの世界観を再現したアトラクションやショーが楽しめることです。
また、ハリー・ポッターやスパイダーマンなどの人気作品のエリアもあり、ファンにはたまらない場所です。
USJの年間パスポートを持っていれば、季節に関係なく好きなだけ来園することができ、オフシーズンであれば比較的空いているため、長い時間を過ごすことができます。
USJは、大人か

> 大阪万博楽しい？
[INST] 大阪万博楽しい？ [/INST]  大阪万博は1970年に開催された国際博覧会です。
私は1970年生まれであるため、万博に参加したことはありません。しかし、大阪万博では日本初登場となる宇宙飛行士のアポロ11号によって持ち帰られた月の石や、日本初公開となるエンタープライズ号の船内、世界最高峰のジュネーブ時計が展示されていたこと等、様々な話題を提供してくれた事は事実です。また、大阪万博をきっかけに日本が世界に羽ばたくきっかけとなったことは間違いありません。

> マクナルっておいしい？
[INST] マクナルっておいしい？ [/INST]  マクドナルドは、世界中に店舗を持つファーストフードチェーンの1つです。
そのため、個人の好みや地域の文化によって、味の好みや評価は異なります。
マクドナルドの食品は、調理法や製品によっては、かなりの油分や塩分を含んでいるため、普通の食事のみにしておく方が良いでしょう。

> マクナル嫌いなの？
[INST] マクナル嫌いなの？ [/INST]  マクナルは嫌いではありません。
ただ、彼の作品はあまり聴いたことがありません。

> exit   # "exit" or "quit" or EOFでチャット終了
See you!
(llm-chat) $
```

## JupyterLab (Notebook) 上での動かし方

[llm-chat.ipynb](./llm-chat.ipynb)をJupyterLab (Notebook)に読み込ませたあと、全てのセルを実行してください（⏩）。

依存パッケージやモデルファイルなどのダウンロードが終わった後、チャットができるようになります。

## Q&A

### 長い応答が途中で切れる

[llm-chat.py](./llm-chat.py)内で `print_inference_result()` メソッド呼び出し時に `max_new_tokens` に128より大きな値を指定してください。

```python
# 指定例
llm.print_inference_result(input_text, max_new_tokens=256)
```

`max_new_tokens` は、生成されるトークン数の上限です。
デフォルトでは128なので、もっと大きな値にするとより長い応答を得られます。

### 他のモデルも使いたい

[llm-chat.py](./llm-chat.py)内で `LLM` クラスのインスタンスを作成するとき、コンストラクターに[HuggingFace](https://huggingface.co/)のモデル名を指定してください。

```python
# 指定例
llm = LLM("microsoft/phi-2")
```

デフォルトでは `elyza/ELYZA-japanese-Llama-2-7b-instruct` を使っています。

注意点として、HuggingFaceの認証やログインが不要なモデルを指定してください。
まだ認証処理を入れていないので、認証が必要なモデルはエラーが出ます。

2025/05/11時点で動作確認したモデルは以下のとおりです。

|識別子|モデル名|主な対応言語|URL|
|---|---|---|---|
|`elyza/ELYZA-japanese-Llama-2-7b-instruct`|ELYZA-japanese-Llama-2-7b|日本語/英語|<https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct>|
|`microsoft/phi-2`|Phi-2|英語|<https://huggingface.co/microsoft/phi-2>|
|`cyberagent/open-calm-7b`|OpenCALM|日本語|<https://huggingface.co/cyberagent/open-calm-7b>|
|`rinna/youri-7b-chat`|youri|日本語/英語|<https://huggingface.co/rinna/youri-7b-chat>|

### モデルによって応答がおかしい / エラーが起きる

応答がおかしい場合は、モデルに応じた適切なプロンプトが生成されていない可能性があります。
[llm/llm.py](./llm/llm.py)内で `LLM` クラスの `_prompt()` メソッドがそのモデルに対応したプロンプトを生成していないかもしれないので、適切な条件分岐を入れてプロンプトを生成できるようにしてください。
あとPRください。

エラーが起きる場合は、モデル固有の設定を吸収しきれていない可能性があります。
モデル固有の設定を調整してください。
あとPRください。
