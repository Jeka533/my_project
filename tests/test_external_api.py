"""Тесты для модуля external_api."""

from unittest.mock import MagicMock, patch

import pytest

from scripts.external_api import convert_to_rub, get_amount_in_rub, get_exchange_rate


@patch("scripts.external_api.requests.get")
def test_get_exchange_rate_success(mock_get: MagicMock) -> None:
    """Тест успешного получения курса."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"USD": 0.013}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD")
    assert rate == pytest.approx(76.92, 0.1)


@patch("scripts.external_api.requests.get")
def test_get_exchange_rate_failure(mock_get: MagicMock) -> None:
    """Тест ошибки API."""
    mock_get.side_effect = Exception("API Error")
    assert get_exchange_rate("USD") is None


@patch("scripts.external_api.get_exchange_rate")
def test_convert_to_rub_usd(mock_rate: MagicMock) -> None:
    """Тест конвертации USD -> RUB."""
    mock_rate.return_value = 75.5
    assert convert_to_rub(100, "USD") == 7550.0


def test_convert_to_rub_rub() -> None:
    """Тест: RUB не конвертируется."""
    assert convert_to_rub(1000, "RUB") == 1000.0


@patch("scripts.external_api.get_exchange_rate")
def test_convert_to_rub_failure(mock_rate: MagicMock) -> None:
    """Тест ошибки конвертации."""
    mock_rate.return_value = None
    assert convert_to_rub(100, "USD") is None


@patch("scripts.external_api.convert_to_rub")
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


def test_get_amount_in_rub_invalid() -> None:
    """Тест некорректной транзакции."""
    assert get_amount_in_rub({}) is None
    assert get_amount_in_rub({"wrong": "data"}) is None
    assert get_amount_in_rub({"operationAmount": {}}) is None
