import json
from .IAdvancedAnalysisFileParser import IAdvancedAnalysisFileParser
from ..Models import JsonDict
class JsonSectionParser(IAdvancedAnalysisFileParser):
    """
    Parse JSON files with a specific section into a unified format.
    The section is specified by the 'json_key' or 'caller_key' in the config.
    """
    def parse(self, config: JsonDict) -> JsonDict:
        data = JsonSectionParser._load_json(self.filename)
        caller_data = {}
        for key, value in config.items():
            section = data.get(key, {})
            for k, value in section.items():
                if k == 'variants':
                    caller_data[k] = {}
                    for index, var in enumerate(value):
                        caller_data[k][index] = IAdvancedAnalysisFileParser._format_value(var)
                else:
                    caller_data[k] = IAdvancedAnalysisFileParser._format_value(value)
        return caller_data

    @staticmethod
    def _load_json(path: str) -> JsonDict:
        with open(path, 'r') as f:
            return json.load(f)