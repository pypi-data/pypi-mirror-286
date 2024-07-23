import multiprocessing
import sys
from typing import Optional

import pandas as pd
from datasets import Dataset, load_dataset


def load_json(file_path: str) -> Optional[Dataset]:
    try:
        return load_dataset(
            "json",
            data_files=file_path,
            split="train",
            num_proc=multiprocessing.cpu_count(),
        )
    except Exception as e:
        print(f"Error loading JSON dataset from {file_path}: {e}", file=sys.stderr)
        return None


def load_excel(file_path: str) -> Optional[Dataset]:
    try:
        df = pd.read_excel(file_path).ffill().astype(str)
        return Dataset.from_pandas(df)
    except Exception as e:
        print(f"Error loading Excel dataset from {file_path}: {e}", file=sys.stderr)
        return None
