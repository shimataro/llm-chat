# LLM-chat

いろんなLLMでチャット！

## 動かし方

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

[llm-chat.py](./llm-chat.py)内で `LLM` クラスのインスタンスを作成するとき、コンストラクターの第1引数に[HuggingFace](https://huggingface.co/)のモデル名を指定してください。

```python
# 指定例
llm = LLM("microsoft/phi-2")

# またはキーワードパラメーターで指定
llm = LLM(model_name="microsoft/phi-2")
```

デフォルトでは `elyza/ELYZA-japanese-Llama-2-7b-instruct` を使っています。

### HuggingFaceの認証やログインが必要なモデルを使いたい

[llm-chat.py](./llm-chat.py)内で `LLM` クラスのインスタンスを作成するとき、コンストラクターの第2引数にアクセストークンを指定してください。

```python
# 指定例
llm = LLM("meta-llama/Meta-Llama-3-8B-Instruct", "YOUR_ACCESS_TOKEN")

# またはキーワードパラメーターで指定
llm = LLM(model_name="meta-llama/Meta-Llama-3-8B-Instruct", access_token="YOUR_ACCESS_TOKEN")
```

アクセストークンは、以下の手順で作成してください。

1. [Hugging Face](https://huggingface.co/)にサインアップ＆ログイン
1. [アクセストークン](https://huggingface.co/settings/tokens)のページから[トークンを作成](https://huggingface.co/settings/tokens/new?tokenType=read)
    * "Token type" は "READ" でOK
    * 名前は自分でわかりやすいものを指定（ `LLM Chat` など）
1. 生成された `hf_` で始まる文字列がアクセストークン

アクセストークンは一度しか表示されないので、忘れないように付箋紙にメモしてディスプレイに貼っておいてください。

### どうやってモデルを探せばいいの？

[モデル一覧ページ](https://huggingface.co/models)の "Natural Language Processing" から興味のあるタグを選んでください。

* [Text Generation](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)
* [Translation](https://huggingface.co/models?pipeline_tag=translation&sort=trending)
* [Text2Text Generation](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=trending)

### 動作確認したモデルは？

2025/05/12時点で動作確認したモデルは以下のとおりです。

|モデル名|ジャンル|主な対応言語|アクセストークン|
|---|---|---|---|
|[`elyza/ELYZA-japanese-Llama-2-7b-instruct`](https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct)|Text Generation|日本語/英語|不要|
|[`microsoft/phi-2`](https://huggingface.co/microsoft/phi-2)|Text Generation|英語|不要|
|[`cyberagent/open-calm-7b`](https://huggingface.co/cyberagent/open-calm-7b)|Text Generation|日本語|不要|
|[`rinna/youri-7b-chat`](https://huggingface.co/rinna/youri-7b-chat)|Text Generation|日本語/英語|不要|
|[`meta-llama/Meta-Llama-3-8B-Instruct`](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)|Text Generation|日本語/英語|要|

動作確認できたモデルがあったら教えてください。
あとPRください。

### モデルによって応答がおかしい / エラーが起きる

ハルシネーション的な意味での「おかしい」であれば、まあそういうものだと思ってください。

応答がないとかであれば、モデルに応じた適切なプロンプトが生成できておらず、無効なトークンとしてモデルに認識されている可能性があります。
[llm/llm.py](./llm/llm.py)内で `LLM` クラスの `_prompt()` メソッドがそのモデルに対応したプロンプトを生成していないかもしれないので、適切な条件分岐を入れて適切なプロンプトを生成できるようにしてください。
あとPRください。

エラーが起きる場合は、モデル固有の設定を吸収しきれていない可能性があります。
モデル固有の設定を調整してください。
あとPRください。
