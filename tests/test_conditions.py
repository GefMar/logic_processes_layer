from __future__ import annotations

from unittest.mock import Mock

import pytest

from logic_processes_layer.extensions import ProcessAttr
from logic_processes_layer.extensions.conditions import AttrCondition, FunctionCondition


_TWO = 2


@pytest.fixture
def mock_process_attr():
    return Mock(spec=ProcessAttr)


@pytest.fixture
def mock_context():
    return Mock()


@pytest.fixture
def attr_condition(mock_process_attr):
    return AttrCondition(mock_process_attr)


def test_attr_condition_positive(attr_condition, mock_process_attr, mock_context):
    mock_process_attr.get_value.return_value = True
    assert attr_condition(mock_context) is True
    mock_process_attr.get_value.assert_called_once_with(mock_context)


def test_attr_condition_negative(attr_condition, mock_process_attr, mock_context):
    mock_process_attr.get_value.return_value = False
    assert attr_condition(mock_context) is False
    mock_process_attr.get_value.assert_called_once_with(mock_context)


def test_attr_condition_negated(attr_condition, mock_process_attr, mock_context):
    mock_process_attr.get_value.return_value = True
    condition = ~attr_condition

    assert condition(mock_context) is False
    mock_process_attr.get_value.assert_called_once_with(mock_context)


def test_function_condition_positive(mock_context):
    mock_func = Mock(return_value=True)
    condition: FunctionCondition = FunctionCondition(mock_func)

    assert condition(mock_context) is True
    mock_func.assert_called_once_with(mock_context)


def test_function_condition_negative(mock_context):
    mock_func = Mock(return_value=False)
    condition: FunctionCondition = FunctionCondition(mock_func)

    assert condition(mock_context) is False
    mock_func.assert_called_once_with(mock_context)


def test_function_condition_negated(mock_context):
    mock_func = Mock(return_value=True)
    condition = ~FunctionCondition(mock_func)

    assert condition(mock_context) is False
    mock_func.assert_called_once_with(mock_context)


def test_operator_condition_and(attr_condition, mock_process_attr, mock_context):
    mock_process_attr.get_value.side_effect = (True, True)
    condition1 = attr_condition
    condition2 = attr_condition
    combined_condition = condition1 & condition2

    assert combined_condition(mock_context) is True
    assert mock_process_attr.get_value.call_count == _TWO


def test_operator_condition_or(attr_condition, mock_process_attr, mock_context):
    mock_process_attr.get_value.side_effect = (False, True)
    condition1 = attr_condition
    condition2 = attr_condition
    combined_condition = condition1 | condition2

    assert combined_condition(mock_context) is True
    assert mock_process_attr.get_value.call_count == _TWO


def test_operator_condition_complex(attr_condition, mock_process_attr, mock_context):
    mock_process_attr.get_value.side_effect = (True, False, True)
    condition1 = attr_condition
    condition2 = ~attr_condition
    condition3 = attr_condition
    condition4: FunctionCondition = FunctionCondition(lambda _: True)
    combined_condition = condition1 & (condition2 | condition3) & condition4

    assert combined_condition(mock_context) is True
    assert mock_process_attr.get_value.call_count == _TWO
