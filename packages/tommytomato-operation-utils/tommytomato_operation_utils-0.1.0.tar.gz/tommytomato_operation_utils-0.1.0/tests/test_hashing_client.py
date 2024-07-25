import hashlib
import unittest

from pandas import DataFrame

from tommytomato_utils.hashing_client.hashing_client import HashingClient
from tommytomato_utils.hashing_client.exceptions import (
    InvalidInputTypeError, MissingHashColumnsArgumentError, MissingHashColumnsError
)

# Assuming the HashGenerator class is already defined as provided previously


class TestHashGenerator(unittest.TestCase):

    def setUp(self):
        self.hash_gen = HashingClient()

    def test_list_hash(self):
        values = ['value1', 'value2', 'value3']
        expected_hash = hashlib.sha256("value1:value2:value3".encode('utf-8')).hexdigest()
        self.assertEqual(self.hash_gen.generate_hash(values), expected_hash)

    def test_dataframe_hash(self):
        data = {
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4'],
            'col3': ['value5', 'value6']
        }
        df = DataFrame(data)
        hash_columns = ['col1', 'col2']
        expected_hash_1 = hashlib.sha256("value1:value3".encode('utf-8')).hexdigest()
        expected_hash_2 = hashlib.sha256("value2:value4".encode('utf-8')).hexdigest()

        hashed_df = self.hash_gen.generate_hash(df, hash_columns=hash_columns, column_name='hash')

        self.assertEqual(hashed_df.loc[0, 'hash'], expected_hash_1)
        self.assertEqual(hashed_df.loc[1, 'hash'], expected_hash_2)

    def test_same_input_same_hash(self):
        values = ['value1', 'value2']
        data = {
            'col1': ['value1'],
            'col2': ['value2'],
        }
        df = DataFrame(data)
        hash_columns = ['col1', 'col2']

        list_hash = self.hash_gen.generate_hash(values)
        hashed_df = self.hash_gen.generate_hash(df, hash_columns=hash_columns, column_name='hash')
        dataframe_hash = hashed_df.loc[0, 'hash']

        self.assertEqual(list_hash, dataframe_hash)

    def test_invalid_input_type(self):
        with self.assertRaises(InvalidInputTypeError):
            self.hash_gen.generate_hash(123)  # Invalid input type

    def test_missing_columns_error(self):
        data = {
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4']
        }
        df = DataFrame(data)
        hash_columns = ['col1', 'col3']  # 'col3' does not exist in the DataFrame

        with self.assertRaises(MissingHashColumnsError):
            self.hash_gen.generate_hash(df, hash_columns=hash_columns, column_name='hash')

    def test_missing_hash_columns_argument(self):
        data = {
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4']
        }
        df = DataFrame(data)

        with self.assertRaises(MissingHashColumnsArgumentError):
            self.hash_gen.generate_hash(df, column_name='hash')  # Missing hash_columns argument


if __name__ == '__main__':
    unittest.main()
