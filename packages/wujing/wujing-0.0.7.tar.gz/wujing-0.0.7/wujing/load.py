import os
from typing import Literal
from typing import Optional

from datasets import Dataset, DatasetDict
from icecream import ic
from pydantic import BaseModel, ValidationError, field_validator

from wujing.internal.load_data import load_json, load_excel, load_csv

FILE_TYPE_LOADERS = {
    'json': load_json,
    'jsonl': load_json,
    'xls': load_excel,
    'xlsx': load_excel,
    'csv': load_csv,
}

SUPPORTED_FILE_TYPES = list(FILE_TYPE_LOADERS.keys())

FileTypeLiteral = Literal['json', 'jsonl', 'xls', 'xlsx', 'csv']


class FileParameters(BaseModel):
    file_path: str
    file_type: Optional[FileTypeLiteral] = None

    @field_validator('file_path')
    def check_file_path(cls, value: str) -> str:
        if not value:
            raise ValueError('file_path cannot be empty')
        return value


def get_file_extension(file_path: str) -> str:
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:].lower()  # Remove the leading dot and convert to lower case


def _load_dataset(file_path: str, file_type: Optional[str] = None) -> Optional[Dataset]:
    try:
        params = FileParameters(file_path=file_path, file_type=file_type)
    except ValidationError as e:
        raise ValueError(f"Validation error: {e.errors()}")

    if not params.file_type:
        actual_file_extension = get_file_extension(file_path)
        if actual_file_extension in SUPPORTED_FILE_TYPES:
            params.file_type = actual_file_extension
        else:
            raise ValueError(f"Could not infer file type from extension: {actual_file_extension}")
    else:
        actual_file_extension = get_file_extension(file_path)
        if actual_file_extension != params.file_type:
            raise ValueError(f"The file extension {actual_file_extension} does not match the specified file type {params.file_type}")

    load_function = FILE_TYPE_LOADERS.get(params.file_type)
    if load_function:
        return load_function(params.file_path)
    else:
        raise ValueError(f"Unsupported file type: {params.file_type}")


def load_dataset(*files: str) -> Optional[DatasetDict]:
    def merge_dataset_dicts(*dataset_dicts: DatasetDict) -> DatasetDict:
        merged_dict = DatasetDict()

        for dataset_dict in dataset_dicts:
            for key, dataset in dataset_dict.items():
                if key in merged_dict:
                    raise KeyError(f"Conflict detected for key: {key}")
                merged_dict[key] = dataset

        return merged_dict

    return merge_dataset_dicts(*[_load_dataset(file) for file in files])


if __name__ == '__main__':
    ic(load_dataset("./testdata/person_info_1.json"))
    ic(load_dataset("./testdata/person_info_2.json"))
    ic(load_dataset("./testdata/person_info.xlsx"))
    ic(load_dataset("./testdata/person_info_gbk.csv"))
    ic(load_dataset("./testdata/person_info_1.json", "./testdata/person_info_2.json", "./testdata/person_info.xlsx", "./testdata/person_info_gbk.csv"))
