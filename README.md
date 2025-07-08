# LLM-chat

いろんなLLMでチャット！

## 準備

[pipenv](https://pipenv.pypa.io/en/latest/)が必要です。

```text
$ pipenv sync
Creating a virtualenv for this project
...
✔ Successfully created virtual environment!
Virtualenv location: XXX
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (XXX)...
All dependencies are now up-to-date!
```

## 起動方法

`pipenv run llm-chat` で起動できます。
必要なモデル等がロードされた後 `>` が表示されるので、何か話しかけてください。
出力にプロンプトが表示されることがありますが、とりあえず気にしないでください。生成されたプロンプトの確認のためにあえて残しています。

```text
$ pipenv run llm-chat
Model Name: elyza/ELYZA-japanese-Llama-2-7b-instruct
Access Token: None
Source Language: None
Target Language: None

Loading model...
...

It's time to talk!
Type 'exit' to end the conversation.

> ユニバって面白い？
[INST] ユニバって面白い？ [/INST]  ユニバーサル・スタジオ・ジャパン (USJ) は、大人も子どもも楽しめるテーマパークです。
USJの魅力は、映画やテレビ番組などの人気キャラクターの世界観を再現したアトラクションやショーが楽しめることです。
また、ハリー・ポッターやスパイダーマンなどの人気作品のエリアもあり、ファンにはたまらない場所です。
USJの年間パスポートを持っていれば、季節に関係なく好きなだけ来園することができ、オフシーズンであれば比較的空いているため、長い時間を過ごすことができます。
USJは、大人か

> 大阪万博楽しい？
[INST] 大阪万博楽しい？ [/INST]  大阪万博は1970年に開催された国際博覧会です。
私は1970年生まれであるため、万博に参加したことはありません。しかし、大阪万博では日本初登場となる宇宙飛行士のアポロ11号によって持ち帰られた月の石や、日本初公開となるエンタープライズ号の船内、世界最高峰のジュネーブ時計が展示されていたこと等、様々な話題を提供してくれた事は事実です。また、大阪万博をきっかけに日本が世界に羽ばたくきっかけとなったことは間違いありません。

> お腹空かない？
[INST] お腹空かない？ [/INST]  いいえ、空いています。
お腹が空いたなんて思ったことはありません。
私はいつでも腹を空かせている状態です。

> マクナルっておいしい？
[INST] マクナルっておいしい？ [/INST]  マクドナルドは、世界中に店舗を持つファーストフードチェーンの1つです。
そのため、個人の好みや地域の文化によって、味の好みや評価は異なります。
マクドナルドの食品は、調理法や製品によっては、かなりの油分や塩分を含んでいるため、普通の食事のみにしておく方が良いでしょう。

> マクナル嫌いなの？
[INST] マクナル嫌いなの？ [/INST]  マクナルは嫌いではありません。
ただ、彼の作品はあまり聴いたことがありません。

> exit
See you!
```

## JupyterLab (Notebook) 上での動かし方

[`llm-chat.ipynb`](./llm-chat.ipynb)をJupyterLab (Notebook)で開き、⏩ボタンをクリックして全てのセルを実行してください。

依存パッケージやモデルファイルなどのダウンロードが終わった後、チャットができるようになります。

## オプション一覧

|オプション|意味|規定値|備考|
|---|---|---|---|
|`--model-name`, `-m`|使用するモデル名|[`elyza/ELYZA-japanese-Llama-2-7b-instruct`](https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct)|[Hugging Face](https://huggingface.co/models)の中から選択|
|`--access-token`, `-t`|Hugging Faceのアクセストークン|なし||
|`--language-source`, `-S`|入力の[言語コード](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200)|指定なし|[Text2Text Generation](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=trending)または[Translation](https://huggingface.co/models?pipeline_tag=translation&sort=trending)タスクで有効|
|`--language-target`, `-T`|出力の[言語コード](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200)|指定なし|[Text2Text Generation](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=trending)または[Translation](https://huggingface.co/models?pipeline_tag=translation&sort=trending)タスクで有効|

コマンドラインから指定する場合

```bash
# "--model-name" でモデルを指定
$ pipenv run llm-chat --model-name microsoft/phi-2
# "-m" でも可
$ pipenv run llm-chat -m microsoft/phi-2
```

JupyterLab (Notebook)で動かす場合は、最後のセルの `main()` の呼び出し時に配列で指定してください。

```python
main(["-m", "microsoft/phi-2"])
```

実際の用途は、下のQ&Aを参照してください。

## Q&A

### 長い応答が途中で切れる

[`llm-chat.py`](./llm-chat.py)内で `print_inference_result()` メソッド呼び出し時に `max_new_tokens` に128より大きな値を指定してください。

```python
# 指定例
llm.print_inference_result(input_text, max_new_tokens=256)
```

`max_new_tokens` は、生成されるトークン数の上限です。
デフォルトでは128なので、もっと大きな値にするとより長い応答を得られます。

### 他のモデルを使いたい

デフォルトのモデル（[`elyza/ELYZA-japanese-Llama-2-7b-instruct`](https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct)）以外を使う場合は、起動時にコマンドライン引数 `--model-name` （または `-m` ）を指定してください。

```bash
# "--model-name" でモデルを指定
$ pipenv run llm-chat --model-name microsoft/phi-2
# "-m" でも可
$ pipenv run llm-chat -m microsoft/phi-2
```

```python
# JupyterLab (Notebook)で動かす場合
main(["-m", "microsoft/phi-2"])
```

### どうやってモデルを探せばいいの？

[モデル一覧ページ](https://huggingface.co/models)の "Natural Language Processing" から興味のあるタスクを選んでください。

* [Text Generation](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)
* [Text2Text Generation](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=trending)
* [Translation](https://huggingface.co/models?pipeline_tag=translation&sort=trending)

### 動作確認したモデルはある？

2025/05/13時点で動作確認したモデルは以下のとおりです。
「入力に対して、特にエラーが出ず何かしらの出力が得られた」程度の確認であり、出力の精度などは検証していません。

|モデル名|タスク|日本語対応|アクセストークン|
|---|---|---|---|
|[`cyberagent/open-calm-7b`](https://huggingface.co/cyberagent/open-calm-7b)|Text Generation|○|不要|
|[`elyza/ELYZA-japanese-Llama-2-7b-instruct`](https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct)|Text Generation|○|不要|
|[`facebook/nllb-200-distilled-600M`](https://huggingface.co/facebook/nllb-200-distilled-600M)|Translation|○|不要|
|[`google-t5/t5-small`](https://huggingface.co/google-t5/t5-small)|Translation|×|不要|
|[`google/flan-t5-base`](https://huggingface.co/google/flan-t5-base)|Text2Text Generation|×|不要|
|[`google/gemma-2-2b-jpn-it`](https://huggingface.co/google/gemma-2-2b-jpn-it)|Text Generation|○|要|
|[`google/gemma-7b-it`](https://huggingface.co/google/gemma-7b-it)|Text Generation|△|要|
|[`meta-llama/Meta-Llama-3-8B-Instruct`](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)|Text Generation|△|要|
|[`microsoft/phi-2`](https://huggingface.co/microsoft/phi-2)|Text Generation|×|不要|
|[`rinna/youri-7b-chat`](https://huggingface.co/rinna/youri-7b-chat)|Text Generation|○|不要|

動作確認できたモデルがあったらこの表に載せるので教えてください。
あるいは修正PRください。

### 認証やログインが必要なモデルを使いたい

チャット起動時に、コマンドライン引数 `--access-token` （または `-t` ）でアクセストークンを指定してください。

```bash
# "--access-token" でアクセストークンを指定
$ pipenv run llm-chat --model-name meta-llama/Meta-Llama-3-8B-Instruct --access-token YOUR_ACCESS_TOKEN
# "-t" でも可
$ pipenv run llm-chat -m meta-llama/Meta-Llama-3-8B-Instruct -t YOUR_ACCESS_TOKEN
```

```python
# JupyterLab (Notebook)で動かす場合
main(["-m", "meta-llama/Meta-Llama-3-8B-Instruct", "-t", "YOUR_ACCESS_TOKEN"])
```

アクセストークンは、以下の手順で作成してください。

1. [Hugging Face](https://huggingface.co/)にサインアップ＆ログイン
1. [アクセストークン](https://huggingface.co/settings/tokens)のページから[トークンを作成](https://huggingface.co/settings/tokens/new?tokenType=read)
    * "Token type" に "READ" を指定
    * 名前は自分でわかりやすいものを指定（ `LLM Chat` など）
1. 生成された `hf_` で始まる文字列がアクセストークン

アクセストークンは一度しか表示されないので、忘れないように付箋紙にメモしてディスプレイに貼っておいてください。

### 入力/出力の言語を明示的に指定できる？

`--language-source` （または `-S` ）で入力の言語コードを、 `--language-target` （または `-T` ）で出力の言語コードを指定できます。
言語コードの一覧は[こちら](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200)をご参照ください。

特に[`facebook/nllb-200-distilled-600M`](https://huggingface.co/facebook/nllb-200-distilled-600M)のような翻訳に特化したモデルでは、出力の言語コードを指定しないと想定外の言語で出力される場合があります。

```bash
# "--language-source" / "--language-target" で入出力言語コードを指定
$ pipenv run llm-chat --model-name facebook/nllb-200-distilled-600M --language-source eng_Latn --language-target jpn_Jpan
# "-S" / "-T" でも可
$ pipenv run llm-chat -m facebook/nllb-200-distilled-600M -S eng_Latn -T jpn_Jpan
```

```python
# JupyterLab (Notebook)で動かす場合
main(["-m", "facebook/nllb-200-distilled-600M", "-S", "eng_Latn", "-T", "jpn_Jpan"])
```

これらオプションは、[Text2Text Generation](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=trending)または[Translation](https://huggingface.co/models?pipeline_tag=translation&sort=trending)タスクでのみ有効です。
[Text Generation](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)タスクで指定しても無視されます。

### モデルによって応答がおかしい / エラーが起きる

ハルシネーション的な意味での「おかしい」であれば、まあそういうものだと思ってください。

応答がないとかであれば、[Text Generation](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)タスクでモデルに応じた適切なプロンプトが生成できておらず、無効なトークンとしてモデルに認識されている可能性があります。
[`libs/llm.py`](./libs/llm.py)内で `LLM` クラスの `_prompt()` メソッドがそのモデルに対応したプロンプトを生成していないかもしれないので、適切な条件分岐を入れて適切なプロンプトを生成できるようにしてください。
あとPRください。

あるいは、日本語非対応のモデルで日本語を使用した場合も応答がおかしくなる（応答がない、も含む）場合があります。

エラーが起きる場合は、モデル固有の設定を吸収しきれていない可能性があります。
その場合は固有の設定を調整してください。
あとPRください。

### 自動プロンプト加工を行ってほしくない

バックスラッシュ `\` で始まる文字列が入力されたら、デフォルトのプロンプト加工は行わず、以下の加工をしたものをプロンプトとしてモデルに渡します。

* 先頭のバックスラッシュを除去
* `\n` を改行文字に変換
* `\` の次の文字が `n` 以外なら `\` を除去（ `\あ` → `あ`, `\\` → `\`, `\\n` → `\n` ）

以下のような場合に試してみてください。

* 独自のプロンプトが必要なモデルを使う場合
* デフォルトのプロンプトでは不十分な場合（システムプロンプトを指定したいなど）
* 会話ではなく、入力した文章の続きを生成したい場合

※プロンプト加工を行うのは[Text Generation](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)タスクだけです。
[Text2Text Generation](https://huggingface.co/models?pipeline_tag=text2text-generation&sort=trending)や[Translation](https://huggingface.co/models?pipeline_tag=translation&sort=trending)タスクでは、改行を明示的に含ませたいという意図がなければ本機能は意味がありません（使っても特に害はありません）
