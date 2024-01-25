from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class AttrsData:
    args: tuple
    kwargs: dict
