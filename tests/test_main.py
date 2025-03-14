import json
import pytest
import pandas as pd
from pathlib import Path
from scripts.main import CRM
from unittest.mock import patch


@pytest.fixture
def sample_csv(tmp_path):
    file_path: Path = tmp_path / "test.csv"
    data: str = """col1;col2;col3\n1;2;3\n4;5;6\n7;8;9"""
    file_path.write_text(data)
    return str(file_path)

@pytest.fixture
def headers_eng():
    return {("col1",): "column1", ("col2",): "column2", ("col3",): "column3"}

@pytest.fixture
def crm(sample_csv, tmp_path, headers_eng):
    return CRM(
        sample_csv,
        str(tmp_path),
        headers_eng,
        [],
        [],
        [],
        []
    )


def test_convert_csv_to_dict(crm: CRM) -> None:
    """
    Tests the `convert_csv_to_dict` method.

    It verifies that the `convert_csv_to_dict` method correctly reads a
    csv file and returns a list of dictionaries.

    :param crm: A fixture for an instance of `CRM`
    :return None
    """
    result: list = crm.convert_csv_to_dict()
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == {"column1": "1", "column2": "2", "column3": "3"}


def test_rename_columns(crm: CRM) -> None:
    """
    Tests the `rename_columns` method.

    It verifies that the `rename_columns` method correctly renames the
    columns of a given DataFrame according to the provided headers.

    :param crm: A fixture for an instance of `CRM`
    :return None
    """
    df: pd.DataFrame = pd.DataFrame({"col1": [1], "col2": [2], "col3": [3]})
    crm.rename_columns(df)
    assert list(df.columns) == ["column1", "column2", "column3"]


def test_change_type() -> None:
    """
    Tests the `change_type` method of the `CRM` class.

    It verifies that the `change_type` method correctly converts the data
    types of values in the given dictionary according to the specified
    lists of types in the CRM instance. Specifically, it checks the conversion
    of float, bool, int, and date types.

    :return None
    """
    crm: CRM = CRM(
        "",
        "",
        {},
        ["float_col"],
        ["bool_col"],
        ["int_col"],
        ["date_col"]
    )
    data: dict = {
        "float_col": "12,34",
        "bool_col": "True",
        "int_col": "42",
        "date_col": "2023-01-01"
    }
    crm.change_type(data)
    assert isinstance(data["float_col"], float)
    assert isinstance(data["bool_col"], bool)
    assert isinstance(data["int_col"], int)
    assert isinstance(data["date_col"], str)


def test_save_data_to_file(crm: CRM, tmp_path: Path) -> None:
    """
    Tests the `save_data_to_file` method.

    It verifies that the `save_data_to_file` method correctly saves the given
    data to a file in the specified directory. The file name is a combination
    of the input file name and the chunk number.

    :param crm: A fixture for an instance of `CRM`
    :param tmp_path: A fixture for a temporary path
    :return None
    """
    sample_data: list = [{"key": "value"}]
    crm.save_data_to_file(1, sample_data)
    output_file: Path = tmp_path / "test.csv_1.json"
    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == sample_data


def test_delete_all_data_from_db() -> None:
    """
    Tests the `delete_all_data_from_db` method.

    It verifies that the `delete_all_data_from_db` method correctly deletes all
    data from the database for the given file name.

    :return None
    """
    with patch("scripts.main.get_client") as mock_client:
        mock_instance = mock_client.return_value
        CRM.delete_all_data_from_db("test_file.py")
        mock_instance.query.assert_called_once()
