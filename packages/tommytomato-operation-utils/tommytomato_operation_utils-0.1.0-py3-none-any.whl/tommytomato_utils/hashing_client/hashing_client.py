from typing import List, Union

from pandas import DataFrame, Series

from tommytomato_utils.hashing_client.constants import (
    HASHING_FIELD_SEPARATOR,
    HASHING_FUNCTION_ALGORITHM
)
from tommytomato_utils.hashing_client.exceptions import (
    InvalidInputTypeError,
    MissingHashColumnsArgumentError,
    MissingHashColumnsError
)


class HashingClient:
    """
    Client to generate a hash based on either a list of string values or specific columns of a
    DataFrame.
    """

    def __init__(self):
        pass

    @staticmethod
    def generate_hash(
        input_data: Union[List[str], DataFrame],
        hash_columns: List[str] = None,
        column_name: str = 'hash'
    ) -> Union[str, DataFrame]:
        """
        Generates a hash based on a list of string values or specific columns of a DataFrame.

        Args:
            input_data (Union[List[str], DataFrame]): List of string values to hash or DataFrame
            containing the columns to hash.
            hash_columns (List[str], optional): List of columns to hash in the DataFrame. Required
            if input_data is a DataFrame.
            column_name (str, optional): Name of the column to store the hash in the DataFrame.
            Defaults to 'hash'.

        Returns:
            Union[str, DataFrame]: The resulting hash as a string if input_data is a list of
            strings, or the DataFrame with the hash column if input_data is a DataFrame.

        Raises:
            InvalidInputTypeError: If input_data is neither a list nor a DataFrame.
            MissingHashColumnsArgumentError: If hash_columns are not provided for a DataFrame.
            MissingHashColumnsError: If any specified hash_columns are not found in the DataFrame.
        """
        if isinstance(input_data, list):
            return HashingClient._get_list_hash(input_data)
        elif isinstance(input_data, DataFrame):
            if hash_columns is None:
                raise MissingHashColumnsArgumentError()
            return HashingClient._get_dataframe_hash(input_data, column_name, hash_columns)
        else:
            raise InvalidInputTypeError(input_data)

    @staticmethod
    def _get_list_hash(values: List[str]) -> str:
        """
        Generates a hash based on a list of string values.

        Args:
            values (List[str]): List of string values to hash.

        Returns:
            str: The resulting hash.
        """

        def hash_series(input_str: str) -> str:
            return HASHING_FUNCTION_ALGORITHM(input_str.encode("utf-8")).hexdigest()

        concatenated_values = HASHING_FIELD_SEPARATOR.join(map(str, values))
        return hash_series(concatenated_values)

    @staticmethod
    def _get_dataframe_hash(
        dataframe: DataFrame, column_name: str, hash_columns: List[str]
    ) -> DataFrame:
        """
        Generates a hash based on specific columns of a DataFrame.

        Args:
            dataframe (DataFrame): DataFrame containing the columns to hash.
            column_name (str): Name of the column to store the hash in the DataFrame.
            hash_columns (List[str]): List of columns to hash in the DataFrame.

        Returns:
            DataFrame: The DataFrame with the hash column added.

        Raises:
            MissingHashColumnsError: If any specified hash_columns are not found in the DataFrame.
        """

        def create_hash_from_series(string_value: str) -> str:
            return HASHING_FUNCTION_ALGORITHM(string_value.encode("utf-8")).hexdigest()

        try:
            concatenated_columns = Series(
                map(
                    HASHING_FIELD_SEPARATOR.join,
                    dataframe[hash_columns].astype(str).values.tolist(),
                ),
                index=dataframe.index,
            )
        except KeyError:
            raise MissingHashColumnsError(dataframe, hash_columns)

        dataframe[column_name] = concatenated_columns.apply(create_hash_from_series)
        return dataframe
