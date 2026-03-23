"""Тесты для модуля external_api."""

from unittest.mock import MagicMock, patch

from scripts.external_api import convert_currency, get_amount_in_rub


@patch("scripts.external_api.requests.get")
def test_convert_currency_success(mock_get: MagicMock) -> None:
    """Тест успешной конвертации валюты."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 100},
        "info": {"rate": 92.5},
        "result": 9250.0
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_currency(100.0, "USD", "RUB")
    assert result == 9250.0
    mock_get.assert_called_once()


@patch("scripts.external_api.requests.get")
def test_convert_currency_failure(mock_get: MagicMock) -> None:
    """Тест ошибки API при конвертации."""
    mock_get.side_effect = Exception("API Error")
    result = convert_currency(100.0, "USD", "RUB")
    assert result is None


@patch("scripts.external_api.requests.get")
def test_convert_currency_same_currency(mock_get: MagicMock) -> None:
    """Тест конвертации в ту же валюту (без запроса к API)."""
    result = convert_currency(100.0, "RUB", "RUB")
    assert result == 100.0
    mock_get.assert_not_called()


@patch("scripts.external_api.requests.get")
def test_convert_currency_api_error_response(mock_get: MagicMock) -> None:
    """Тест ответа API с ошибкой."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "success": False,
        "error": {"info": "Invalid currency code"}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_currency(100.0, "XXX", "RUB")
    assert result is None


@patch("scripts.external_api.convert_currency")
def test_get_amount_in_rub_success(mock_convert: MagicMock) -> None:
    """Тест успешной обработки транзакции."""
    mock_convert.return_value = 7500.0
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }
    assert get_amount_in_rub(transaction) == 7500.0
    mock_convert.assert_called_once_with(100.0, "USD", "RUB")


def test_get_amount_in_rub_rub_transaction() -> None:
    """Тест транзакции в рублях (без конвертации)."""
    transaction = {
        "operationAmount": {
            "amount": "5000.00",
            "currency": {"code": "RUB"},
        }
    }
    assert get_amount_in_rub(transaction) == 5000.0


def test_get_amount_in_rub_invalid() -> None:
    """Тест некорректной транзакции."""
    assert get_amount_in_rub({}) is None
    assert get_amount_in_rub({"wrong": "data"}) is None
    assert get_amount_in_rub({"operationAmount": {}}) is None
