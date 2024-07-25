# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .trading.execution_report import ExecutionReport

__all__ = ["DropCopyExecutionReport"]


class DropCopyExecutionReport(Event):
    payload: Optional[ExecutionReport] = None
