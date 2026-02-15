from typing import List, Dict, Any, TypedDict


class EmailGraphState(TypedDict):
    emails: List[dict[str, Any]]
    decisions: List[dict[str, Any]]
    stats: Dict[str, int]
