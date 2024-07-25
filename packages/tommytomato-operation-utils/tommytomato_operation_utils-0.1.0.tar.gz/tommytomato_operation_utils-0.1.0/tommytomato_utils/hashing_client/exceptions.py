from typing import List

from pandas import DataFrame


class HashingError(Exception):
    pass


class InvalidInputTypeError(HashingError):
    def __init__(self, input_data):
        super().__init__(
            f"Invalid input type: {type(input_data).__name__}. "
            f"Expected list or DataFrame."
        )


class MissingHashColumnsError(HashingError):
    def __init__(self, dataframe: DataFrame, hash_columns: List[str]):
        missing_columns = [col for col in hash_columns if col not in dataframe.columns]
        super().__init__(
            '\nMissing columns for hash generation.'
            f'\nDataFrame columns: {dataframe.columns.tolist()}\n\n'
            f'Missing columns: {missing_columns}\n\n'
        )


class MissingHashColumnsArgumentError(HashingError):
    def __init__(self):
        super().__init__("hash_columns must be provided when input_data is a DataFrame.")
