from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class FlyerContext:
    """
    システム全体のコンテキスト（将来的な拡張用）
    """
    session_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


global_context = FlyerContext()
