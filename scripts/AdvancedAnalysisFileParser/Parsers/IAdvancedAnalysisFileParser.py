from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Any
from ..Models import JsonDict
class IAdvancedAnalysisFileParser(ABC):
    def __init__(self,config:JsonDict, filename: str) -> None:
        if not filename:
            raise ValueError("Filename cannot be empty")
        if not isinstance(filename, str):
            raise TypeError(f"Filename must be a string, got {type(filename).__name__}")
        if not filename.lower().endswith(('.json', '.tsv')):
            raise ValueError("Filename must be in lowercase")
        input_dir = config.get("input_dir", ".")
        file_path = os.path.join(input_dir, filename)
        #check if the file exists on path
        if not os.path.exists(file_path):
            base = Path(__file__).resolve().parent.parent
            file_path = os.path.join(base, file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
        self.filename: str = file_path
        
    @abstractmethod
    def parse(self, config: JsonDict) -> JsonDict:
        pass
    
    @staticmethod
    def _format_value(v: Any) -> Any:
        if isinstance(v, dict):
            return {k: IAdvancedAnalysisFileParser._format_value(v) for k, v in v.items()}
        if isinstance(v, list):
            clean = [IAdvancedAnalysisFileParser._format_value(x) for x in v if x not in ("", None)]
            return clean or None
        if isinstance(v, str):
            low = v.lower()
            if low == "true":
                return True
            if low == "false":
                return False
            if low in ("none", "null", ""):
                return None
            try:
                return int(v)
            except ValueError:
                pass
            try:
                return round(float(v), 2)
            except ValueError:
                return v
        if isinstance(v, float):
            return round(v, 2)
        #if isinstance(v, bool):
        #if isinstance(v, int):
        return v