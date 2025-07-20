from dataclasses import dataclass
from typing import Optional,Dict
from .FieldCondition import FieldCondition

@dataclass
class SectionConfig:
    include_all_fields: bool = False
    fields: Optional[Dict[str, FieldCondition]] = None