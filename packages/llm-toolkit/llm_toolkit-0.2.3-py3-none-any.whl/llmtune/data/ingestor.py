import csv
from abc import ABC, abstractmethod

import ijson
from datasets import Dataset, concatenate_datasets, load_dataset


def get_ingestor(data_type: str):
    if data_type == "json":
        return JsonIngestor
    elif data_type == "jsonl":
        return JsonlIngestor
    elif data_type == "csv":
        return CsvIngestor
    elif data_type == "huggingface":
        return HuggingfaceIngestor
    else:
        raise ValueError(f"'type' must be one of 'json', 'jsonl', 'csv', or 'huggingface', you have {data_type}")


class Ingestor(ABC):
    @abstractmethod
    def to_dataset(self) -> Dataset:
        pass


class JsonIngestor(Ingestor):
    def __init__(self, path: str):
        self.path = path

    def _json_generator(self):
        with open(self.path, "rb") as f:
            for item in ijson.items(f, "item"):
                yield item

    def to_dataset(self) -> Dataset:
        return Dataset.from_generator(self._json_generator)


class JsonlIngestor(Ingestor):
    def __init__(self, path: str):
        self.path = path

    def _jsonl_generator(self):
        with open(self.path, "rb") as f:
            for item in ijson.items(f, "", multiple_values=True):
                yield item

    def to_dataset(self) -> Dataset:
        return Dataset.from_generator(self._jsonl_generator)


class CsvIngestor(Ingestor):
    def __init__(self, path: str):
        self.path = path

    def _csv_generator(self):
        with open(self.path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def to_dataset(self) -> Dataset:
        return Dataset.from_generator(self._csv_generator)


class HuggingfaceIngestor(Ingestor):
    def __init__(self, path: str):
        self.path = path

    def to_dataset(self) -> Dataset:
        ds = load_dataset(self.path)
        return concatenate_datasets(ds.values())
