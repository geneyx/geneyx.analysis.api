from typing import Any
from .IAdvancedAnalysisFileParser import IAdvancedAnalysisFileParser
from ..Models import JsonDict
# --- Parser Implementations ---
class OneLineTsvParser(IAdvancedAnalysisFileParser):
    def parse(self,  config: JsonDict) -> JsonDict:
        with open(self.filename, 'r') as f:
            headers = f.readline().strip().split('\t')
            values = f.readline().strip().split('\t')
        # Format the values and return as a dictionary
        return {h: IAdvancedAnalysisFileParser._format_value(v) for h, v in zip(headers, values) }
