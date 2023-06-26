import os
import re
import sys
import json
import datetime
import itertools
import contextlib
import numpy as np
from __init__ import *
from typing import Generator
from pandas import DataFrame, read_csv
from __init__rn_stagehistories import *
from clickhouse_connect import get_client


class RnStagehistories(object):
    def __init__(self, filename: str, folder: str, headers_eng: dict, list_of_float_type: list,
                 list_of_bool_type: list, list_of_int_type: list, list_of_date_type: list):
        self.filename: str = filename
        self.folder: str = folder
        self.HEADERS_ENG: dict = headers_eng
        self.LIST_OF_FLOAT_TYPE: list = list_of_float_type
        self.LIST_OF_BOOL_TYPE: list = list_of_bool_type
        self.LIST_OF_INT_TYPE: list = list_of_int_type
        self.LIST_OF_DATE_TYPE: list = list_of_date_type

    @staticmethod
    def delete_all_data_from_db(file):
        """
        Delete all data from database that update data.
        """
        client = get_client(host='clickhouse', database='crm', username='admin', password='6QVnYsC4iSzz')
        client.query(f"ALTER TABLE {os.path.basename(file).replace('.py', '')} DELETE WHERE versionnumber is not null")
        client.close()

    @staticmethod
    def divide_chunks(list_data: list, chunk: int) -> Generator:
        """
        Divide by chunks of a list.
        """
        for i in range(0, len(list_data), chunk):
            yield list_data[i:i + chunk]

    @staticmethod
    def convert_format_date(date: str) -> str:
        """
        Convert to a date type.
        """
        for date_format in date_formats:
            with contextlib.suppress(ValueError):
                return str(datetime.datetime.strptime(date, date_format).date())
        return date

    @staticmethod
    def convert_to_int(int_value: str) -> int:
        """
        Convert a value to integer.
        """
        with contextlib.suppress(ValueError):
            return int(int_value)

    def rename_columns(self, df: DataFrame) -> None:
        """
        Rename of a columns.
        """
        dict_columns_eng: dict = {}
        for column, columns in itertools.product(df.columns, HEADERS_ENG):
            for column_eng in columns:
                if column == column_eng:
                    dict_columns_eng[column] = self.HEADERS_ENG[columns]
        df.rename(columns=dict_columns_eng, inplace=True)

    def convert_csv_to_dict(self) -> list:
        """
        Csv data representation in json.
        """
        df: DataFrame = read_csv(self.filename, low_memory=False, dtype=str, delimiter=';')
        df.replace({np.NAN: None}, inplace=True)
        self.rename_columns(df)
        return df.to_dict('records')

    def change_type(self, data: dict) -> None:
        """
        Change a type of data.
        """
        for key, value in data.items():
            with contextlib.suppress(Exception):
                if key in self.LIST_OF_FLOAT_TYPE:
                    data[key] = float(re.sub(" +", "", value).replace(',', '.'))
                elif key in self.LIST_OF_DATE_TYPE:
                    data[key] = self.convert_format_date(value)
                elif key in self.LIST_OF_BOOL_TYPE:
                    data[key] = eval(value)
                elif key in self.LIST_OF_INT_TYPE:
                    data[key] = self.convert_to_int(value)

    def save_data_to_file(self, i: int, chunk_data: list) -> None:
        """
        Save a data to a file.
        """
        basename: str = os.path.basename(self.filename)
        output_file_path: str = os.path.join(self.folder, f'{basename}_{i}.json')
        with open(f"{output_file_path}", 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, ensure_ascii=False, indent=4)

    def main(self, file) -> None:
        """
        Parse data from CSV file. And split it by chunks.
        """
        parsed_data: list = self.convert_csv_to_dict()
        divided_parsed_data: list = list(self.divide_chunks(parsed_data, 50000))
        # self.delete_all_data_from_db(file)
        for index, chunk_parsed_data in enumerate(divided_parsed_data):
            for dict_data in chunk_parsed_data:
                self.change_type(dict_data)
                dict_data['updates'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data_to_file(index, chunk_parsed_data)


if __name__ == "__main__":
    rn_stagehistories: RnStagehistories = RnStagehistories(os.path.abspath(sys.argv[1]), sys.argv[2], HEADERS_ENG,
                                                           LIST_OF_FLOAT_TYPE, LIST_OF_BOOL_TYPE, LIST_OF_INT_TYPE,
                                                           LIST_OF_DATE_TYPE)
    rn_stagehistories.main(__file__)
