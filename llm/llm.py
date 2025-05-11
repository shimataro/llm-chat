from typing import Generator
import threading

import torch
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
from transformers.generation.streamers import TextIteratorStreamer


class LLM:
    def __init__(self, model_name: str = "elyza/ELYZA-japanese-Llama-2-7b-instruct"):
        """ LLMの初期化

        :param model_name: モデル名
        """
        self._model_name = model_name

        dtype: str | torch.dtype = "auto"
        if torch.cuda.is_available():
            # CUDAが有効ならfloat16を使う（"auto"のままだとV100環境でfloat32を選ぶことがある）
            dtype = torch.float16

        # トークナイザーとモデルを読み込み
        self._model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=dtype,
        )
        self._tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)


    def infer(self, input_text: str, max_new_tokens: int=128, do_sample: bool=True, temperature: float=0.7, top_p: float=0.9) -> Generator[str, None, None]:
        """ 推論

        :param input_text: 入力テキスト
        :param max_new_tokens: 生成する最大トークン数
        :param do_sample: 推論結果をサンプリングするか？Falseなら常に確率の一番高いトークンのみを出力する（結果は決定的になる）
        :param temperature: サンプリングの多様性を制御する温度パラメーター
        :param top_p: nucleus samplingの確率閾値
        :return: トークンのジェネレーター

        Examples:
            >>> for token in llm.infer("こんにちは。"):
            ...     print(token, end="", flush=True)
        """
        tokenizer = self._tokenizer
        model = self._model

        # プロンプト生成→トークン生成→GPUメモリーに転送
        prompt = self._prompt(input_text)
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        # 出力取得用のストリーマー
        streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

        thread = threading.Thread(
            target=model.generate,
            kwargs={
                **inputs,
                "streamer": streamer,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": do_sample,
            }
        )
        thread.start()

        for token in streamer:
            yield token


    def print_inference_result(self, input_text: str, max_new_tokens: int=128, do_sample: bool=True, temperature: float=0.7, top_p: float=0.9) -> None:
        """ 推論結果を出力

        :param input_text: 入力テキスト
        :param max_new_tokens: 生成する最大トークン数
        :param do_sample: 推論結果をサンプリングするか？Falseなら常に確率の一番高いトークンのみを出力する（結果は決定的になる）
        :param temperature: サンプリングの多様性を制御する温度パラメーター
        :param top_p: nucleus samplingの確率閾値
        """
        # 入力プロンプト
        for token in self.infer(input_text, max_new_tokens, do_sample, temperature, top_p):
            # トークンを1つずつ出力
            print(token, end="", flush=True)

        # 出力の終端
        print()


    def _prompt(self, input_text: str) -> str:
        """ 入力文字列から、モデルに合わせたプロンプトを生成する

        :param input_text: 入力テキスト
        :return: プロンプト
        """

        # chat_template に対応していれば使う（Mistral, Gemmaなど）
        if hasattr(self._tokenizer, "chat_template"):
            try:
                return self._tokenizer.apply_chat_template(
                    [
                        {"role": "user", "content": input_text},
                    ],
                    tokenize=False,
                    add_generation_prompt=True,
                )
            except Exception:
                # fallback
                pass

        # モデルに合わせたプロンプトを生成
        model_name = self._model_name.lower()
        if "elyza" in model_name:
            return f"[INST] {input_text} [/INST]"

        if "rinna" in model_name:
            return (
                f"ユーザー: {input_text}\n"
                "システム: "
            )

        if "llama-2" in model_name or "llama2" in model_name or "mistral" in model_name or "gemma" in model_name:
            return f"<s>[INST] {input_text} [/INST]</s>"

        if "openchat" in model_name:
            return f"<|user|>\n{input_text}\n<|assistant|>\n"

        if "llama-3" in model_name or "llama3" in model_name:
            return (
                "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
                f"{input_text}\n"
                "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
            )

        # デフォルト（そのまま）
        return input_text
