from __future__ import annotations

from unittest.mock import patch

import pytest

from .examples.processors.process_with_conditions import NotifyClientProcess, OrderStatusProcess


@pytest.mark.parametrize(
    argnames="is_completed, client_agreed, order_amount, should_notify",
    argvalues=(
        (True, True, 150, True),
        (True, False, 150, True),
        (True, True, 50, True),
        (True, False, 50, False),
        (False, True, 150, False),
        (False, False, 150, False),
    ),
    ids=(
        "Both completed and delayed, amount > 100 -> Notify",
        "Completed but not delayed, amount > 100 -> Notify",
        "Both completed and delayed, amount <= 100 -> No Notify",
        "Completed but not delayed, amount <= 100 -> No Notify",
        "Not completed, delayed, amount > 100 -> No Notify",
        "Not completed, not delayed, amount > 100 -> No Notify",
    ),
)
def test_order_status_process(is_completed, client_agreed, order_amount, should_notify):
    with patch.object(NotifyClientProcess, "run", return_value=None) as mock_notify_run:
        process = OrderStatusProcess(
            is_completed=is_completed,
            client_agreed_to_notifications=client_agreed,
            order_amount=order_amount,
        )
        process()

        if should_notify:
            mock_notify_run.assert_called_once()
        else:
            mock_notify_run.assert_not_called()
