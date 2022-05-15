from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Version:
    arch: str
    decomposed: List[int]
    go_tags: str
    go_version: str
    is_beta: bool
    is_git: bool
    linking: str
    os: str
    version: str
