from typing import List

temp_blocklist = []


def get_blocklist() -> List[str]:
    return temp_blocklist


def add_to_blocklist(jti: str) -> None:
    temp_blocklist.append(jti)
