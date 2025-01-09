from __future__ import annotations

import dataclasses

from logic_processes_layer import BaseProcessor
from logic_processes_layer.extensions import InitMapper, ProcessAsSubprocess, ProcessAttr
from logic_processes_layer.extensions.conditions import AttrCondition, FunctionCondition


_ONE_H = 100


@dataclasses.dataclass
class NotifyClientProcess(BaseProcessor):
    notification_message: str

    def run(self): ...  # noqa: WPS428


_order_is_completed_condition: AttrCondition = AttrCondition(ProcessAttr("is_completed"))
_order_amount_condition: FunctionCondition = FunctionCondition(lambda context: context.process.order_amount > _ONE_H)
_client_agreed_condition: AttrCondition = AttrCondition(ProcessAttr("client_agreed_to_notifications"))
_combined_condition = _order_is_completed_condition & (_order_amount_condition | _client_agreed_condition)

_notify_client_process = ProcessAsSubprocess(
    process_cls=NotifyClientProcess,
    init_mapper=InitMapper(notification_message=ProcessAttr("notification_message")),
    conditions=(_combined_condition,),
)


@dataclasses.dataclass
class OrderStatusProcess(BaseProcessor):
    is_completed: bool
    client_agreed_to_notifications: bool
    order_amount: float
    notification_message: str = dataclasses.field(init=False, default="Order completed successfully!")

    post_run = (_notify_client_process,)

    def run(self): ...  # noqa: WPS428
