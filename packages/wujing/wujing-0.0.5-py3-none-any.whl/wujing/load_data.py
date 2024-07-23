import os
from typing import Literal
from typing import Optional

from datasets import Dataset, DatasetDict
from pydantic import BaseModel, ValidationError, field_validator

from wujing.internal.load_data import load_json, load_excel

FILE_TYPE_LOADERS = {
    'json': load_json,
    'jsonl': load_json,
    'xls': load_excel,
    'xlsx': load_excel,
}

SUPPORTED_FILE_TYPES = list(FILE_TYPE_LOADERS.keys())

FileTypeLiteral = Literal['json', 'jsonl', 'xls', 'xlsx']


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


def load_dataset(file_path: str, file_type: Optional[str] = None) -> Optional[Dataset]:
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


def load_datasets(*files: str) -> Optional[DatasetDict]:
    return DatasetDict({file: load_dataset(file) for file in files})


if __name__ == '__main__':
    print(load_dataset("./testdata/person_info_1.json"))
    print(load_dataset("./testdata/person_info_2.json"))
    print(load_datasets("./testdata/person_info_1.json", "./testdata/person_info_2.json"))
