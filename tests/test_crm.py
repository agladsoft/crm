import csv
import json
import pytest
from pathlib import Path
from unittest.mock import Mock
from requests.models import Response
from requests_ntlm import HttpNtlmAuth
from typing import Optional, Union, List
from scripts.crm import (
    CrmClient, StageHistory, GapPowerbiOption, Teams,
    Lead, Interview, Opportunity, Systemuser, Businessunits, Account,
    OpportunitySalesProcesses, ProcesStages
)


class MockResponse(Response):
    def __init__(self, status_code: int, json_data: Optional[Union[list, dict]] = None, text: Optional[str] = None):
        super().__init__()
        self.status_code = status_code  # Родной атрибут Response

        # Устанавливаем `_content`, чтобы `text` и `json()` работали корректно
        if json_data is not None:
            self._content = json.dumps(json_data).encode('utf-8')  # JSON в байты
        elif text is not None:
            self._content = text.encode('utf-8')  # Обычный текст в байты
        else:
            self._content = b''

    def json(self, **kwargs):
        try:
            return json.loads(self.content)  # `self.content` аналогичен `requests.Response`
        except json.JSONDecodeError as e:
            raise ValueError("No valid JSON data provided") from e

    @property
    def text(self):
        return self.content.decode('utf-8') if self.content else ""


@pytest.fixture
def crm_client() -> callable:
    return CrmClient()


@pytest.fixture
def entities(crm_client: callable) -> List[callable]:
    return [
        StageHistory(crm_client),
        GapPowerbiOption(crm_client),
        Lead(crm_client),
        Interview(crm_client),
        Opportunity(crm_client),
        Systemuser(crm_client),
        Businessunits(crm_client),
        Account(crm_client),
        OpportunitySalesProcesses(crm_client),
        ProcesStages(crm_client),
        Teams(crm_client)
    ]


@pytest.fixture
def stage_history(crm_client: callable) -> callable:
    return StageHistory(crm_client=crm_client)


def test_crm_client_auth(crm_client: callable) -> None:
    """
    Tests `CrmClient.get_auth()` method.

    It verifies that the returned `HttpNtlmAuth` instance has correct
    username and password.

    :param crm_client: mocked `CrmClient` instance
    :return None
    """
    auth: HttpNtlmAuth = crm_client.get_auth()
    assert auth.username == 'first\\request'
    assert auth.password == 'Edc789'


def test_save_to_csv(stage_history: callable, mocker: Mock, tmp_path: Path) -> None:
    """
    Tests `save_to_csv` method.

    It verifies that the `save_to_csv` method writes a correct csv file.

    :param stage_history: an instance of StageHistory
    :param mocker: fixture for mocking
    :param tmp_path: fixture for temporary path
    :return None
    """
    stage_history.data_root_path = str(tmp_path)
    test_data: dict = {"value": [{"rn_stagehistoryid": "1", "rn_name": "Test"}]}
    mock_response: MockResponse = MockResponse(
        status_code=200,
        json_data=test_data
    )
    mocker.patch('requests.get', return_value=mock_response)

    stage_history.save_to_csv()

    csv_file: Path = Path(stage_history.csv_file)
    assert csv_file.exists()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader: csv.DictReader = csv.DictReader(f, delimiter=';')
        rows: List[dict] = list(reader)
        assert len(rows) == 1
        assert rows[0]['rn_stagehistoryid'] == '1'
        assert rows[0]['rn_name'] == 'Test'


def test_move_files(stage_history: StageHistory, tmp_path: Path) -> None:
    """
    Tests `move_files` method.

    It verifies that the `move_files` method moves a file from the
    `data_root_path` to its parent directory.

    :param stage_history: an instance of StageHistory
    :param tmp_path: fixture for temporary path
    :return None
    """
    stage_history.data_root_path = str(tmp_path)

    source_file: Path = tmp_path / "rn_stagehistories.csv"
    target_dir: Path = tmp_path / "../"
    source_file.write_text("test")

    stage_history.move_files()

    assert not source_file.exists()
    assert (target_dir / "rn_stagehistories.csv").exists()


def test_get_dto_row(stage_history: StageHistory) -> None:
    """
    Tests the `get_dto_row` method.

    It verifies that the method correctly filters out fields not present
    in the header and applies any necessary modifications to the values.

    :param stage_history: An instance of StageHistory used to call the method
    :return: None
    """
    row: dict = {"rn_stagehistoryid": "1", "rn_name": "Test", "extra": "remove"}
    header: list = ["rn_stagehistoryid", "rn_name"]
    dto_row: dict = stage_history.get_dto_row(row, header)
    assert "extra" not in dto_row
    assert dto_row["rn_stagehistoryid"] == "1"
    assert dto_row["rn_name"] == "Test"


def test_all_classes_used(entities: List[callable], mocker: Mock, tmp_path: Path) -> None:
    """
    Tests that the `save_to_csv` method works correctly for all entities.

    It verifies that the `save_to_csv` method writes a correct csv file
    for each entity in the `entities` list by mocking the HTTP response
    and checking that the file is created.

    :param entities: A list of callable entities to test
    :param mocker: Fixture for mocking HTTP requests
    :param tmp_path: Fixture for temporary path
    :return None
    """
    for entity in entities:
        entity.data_root_path = str(tmp_path)
        test_data: dict = {"value": [{"id": "1", "name": "Test"}]}
        mock_response: MockResponse = MockResponse(
            status_code=200,
            json_data=test_data
        )
        mocker.patch('requests.get', return_value=mock_response)

        entity.save_to_csv()

        csv_file = Path(entity.csv_file)
        assert csv_file.exists()