import pytest
import requests
import requests_mock
from racs.racs_exceptions import NoUpdatesMadeException
from racs.racs import Racs
import warnings


@pytest.fixture
def racs():
    return Racs(resource="test_resource", dataset="test_dataset")


def test_create_post_success(racs):
    with requests_mock.Mocker() as m:
        m.post("https://racs.rest/v3?resource=test_resource&dataset=test_dataset", json={"success": True})
        data = {"key": "value"}
        response = racs.create_post(data)
        assert response == {"success": True}


def test_create_post_no_data(racs):
    with pytest.raises(ValueError, match='Argument "data" is required'):
        racs.create_post()


def test_create_file_success(racs):
    with requests_mock.Mocker() as m:
        m.post("https://racs.rest/v3?resource=test_resource&dataset=test_dataset", json={"success": True})
        with pytest.raises(ValueError, match='Argument "file_path" is required'):
            racs.create_file()


def test_read_post_by_id_success(racs):
    with requests_mock.Mocker() as m:
        m.get("https://racs.rest/v3/test_id", json={"id": "test_id"})
        response = racs.read_post_by_id("test_id")
        assert response == {"id": "test_id"}


def test_read_post_by_id_no_id(racs):
    with pytest.raises(ValueError, match='Argument "post_id" is required'):
        racs.read_post_by_id()


def test_read_post_by_filter_success(racs):
    with requests_mock.Mocker() as m:
        m.post("https://racs.rest/v3/get?resource=test_resource&dataset=test_dataset", json={"posts": []})
        filter_data = {"key": "value"}
        response = racs.read_post_by_filter(filter_data)
        assert response.json() == {"posts": []}


def test_read_post_by_filter_no_filter_data(racs):
    with pytest.raises(ValueError, match='Argument "filter_data" is required'):
        racs.read_post_by_filter()


def test_update_post_by_id_no_post_id(racs):
    with pytest.raises(ValueError, match='Argument "post_id" is required'):
        racs.update_post_by_id(None, {"key": "value"})


def test_update_post_by_id_no_update_options(racs):
    with pytest.raises(ValueError, match='Argument "update_options" is required'):
        racs.update_post_by_id("test_id")


def test_update_post_by_id_success(racs):
    with requests_mock.Mocker() as m:
        m.patch("https://racs.rest/v3/test_id", json={"matchedCount": 1, "modifiedCount": 1})
        response = racs.update_post_by_id("test_id", {"key": "value"})
        assert response == {"matchedCount": 1, "modifiedCount": 1}


def test_update_post_by_id_no_updates_made(racs):
    with requests_mock.Mocker() as m:
        m.patch("https://racs.rest/v3/test_id", json={"matchedCount": 0, "modifiedCount": 0})
        with pytest.raises(NoUpdatesMadeException):
            racs.update_post_by_id("test_id", {"key": "value"})


def test_update_post_by_id_warning(racs):
    with requests_mock.Mocker() as m:
        m.patch("https://racs.rest/v3/test_id", json={"matchedCount": 2, "modifiedCount": 1})
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            racs.update_post_by_id("test_id", {"key": "value"})
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "matchedCount (2) is greater than modifiedCount (1)" in str(w[-1].message)


def test_update_post_by_filter_no_filter_data(racs):
    with pytest.raises(ValueError, match='Argument "filter_data" is required'):
        racs.update_post_by_filter(None, {"key": "value"})


def test_update_post_by_filter_no_update_options(racs):
    with pytest.raises(ValueError, match='Argument "update_options" is required'):
        racs.update_post_by_filter({"key": "value"})


def test_update_post_by_filter_success(racs):
    with requests_mock.Mocker() as m:
        m.patch("https://racs.rest/v3?resource=test_resource&dataset=test_dataset",
                json={"matchedCount": 1, "modifiedCount": 1})
        response = racs.update_post_by_filter({"key": "value"}, {"key": "new_value"})
        assert response == {"matchedCount": 1, "modifiedCount": 1}


def test_update_post_by_filter_no_updates_made(racs):
    with requests_mock.Mocker() as m:
        m.patch("https://racs.rest/v3?resource=test_resource&dataset=test_dataset",
                json={"matchedCount": 0, "modifiedCount": 0})
        with pytest.raises(NoUpdatesMadeException):
            racs.update_post_by_filter({"key": "value"}, {"key": "new_value"})


def test_update_post_by_filter_warning(racs):
    with requests_mock.Mocker() as m:
        m.patch("https://racs.rest/v3?resource=test_resource&dataset=test_dataset",
                json={"matchedCount": 2, "modifiedCount": 1})
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            racs.update_post_by_filter({"key": "value"}, {"key": "new_value"})
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "matchedCount (2) is greater than modifiedCount (1)" in str(w[-1].message)
