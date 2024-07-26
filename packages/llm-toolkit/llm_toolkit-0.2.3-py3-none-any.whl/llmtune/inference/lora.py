import csv
import os
from os.path import join
from threading import Thread

import torch
from datasets import Dataset
from peft import AutoPeftModelForCausalLM
from rich.text import Text
from transformers import AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer

from llmtune.inference.generics import Inference
from llmtune.pydantic_models.config_model import Config
from llmtune.ui.rich_ui import RichUI
from llmtune.utils.save_utils import DirectoryHelper


# TODO: Add type hints please!
class LoRAInference(Inference):
    def __init__(
        self,
        test_dataset: Dataset,
        label_column_name: str,
        config: Config,
        dir_helper: DirectoryHelper,
    ):
        self.test_dataset = test_dataset
        self.label_column = label_column_name
        self.config = config

        self.save_dir = dir_helper.save_paths.results
        self.save_path = join(self.save_dir, "results.csv")
        self.device_map = self.config.model.device_map
        self._weights_path = dir_helper.save_paths.weights

        self.model, self.tokenizer = self._get_merged_model(dir_helper.save_paths.weights)

    def _get_merged_model(self, weights_path: str):
        # purge VRAM
        torch.cuda.empty_cache()

        # Load from path

        self.model = AutoPeftModelForCausalLM.from_pretrained(
            weights_path,
            torch_dtype=self.config.model.casted_torch_dtype,
            quantization_config=BitsAndBytesConfig(**self.config.model.bitsandbytes.model_dump()),
            device_map=self.device_map,
            attn_implementation=self.config.model.attn_implementation,
        )

        model = self.model.merge_and_unload()

        tokenizer = AutoTokenizer.from_pretrained(self._weights_path, device_map=self.device_map)

        return model, tokenizer

    def infer_all(self):
        results = []
        prompts = self.test_dataset["formatted_prompt"]
        labels = self.test_dataset[self.label_column]

        # inference loop
        for idx, (prompt, label) in enumerate(zip(prompts, labels)):
            RichUI.inference_ground_truth_display(f"Generating on test set: {idx+1}/{len(prompts)}", prompt, label)

            try:
                result = self.infer_one(prompt)
            except Exception:
                continue
            results.append((prompt, label, result))

        # TODO: seperate this into another method
        header = ["Prompt", "Ground Truth", "Predicted"]
        os.makedirs(self.save_dir, exist_ok=True)
        with open(self.save_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in results:
                writer.writerow(row)

    def infer_one(self, prompt: str) -> str:
        input_ids = self.tokenizer(prompt, return_tensors="pt", truncation=True).input_ids.cuda()

        # stream processor
        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            decode_kwargs={"skip_special_tokens": True},
            timeout=60,  # 60 sec timeout for generation; to handle OOM errors
        )

        generation_kwargs = dict(input_ids=input_ids, streamer=streamer, **self.config.inference.model_dump())

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        result = Text()
        with RichUI.inference_stream_display(result) as live:
            for new_text in streamer:
                result.append(new_text)
                live.update(result)

        return str(result)
