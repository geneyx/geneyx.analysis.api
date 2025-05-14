from .IAdvancedAnalysisFileParser import IAdvancedAnalysisFileParser
from .DragenTruSightOncology500TSVParser import DragenTruSightOncology500TSVParser
from .OneLineTsvParser import OneLineTsvParser
from .JsonSectionParser import JsonSectionParser
from ..Models import JsonDict
class AdvancedAnalysisFileParserFactory:
    """
    Returns the correct IParser implementation based on filename.
    """
    @staticmethod
    def get_parser(config: JsonDict , filename: str) -> IAdvancedAnalysisFileParser:
        lower = filename.lower()
        if lower.endswith("combinedvariantoutput.tsv"):
            return DragenTruSightOncology500TSVParser(config,filename)
        if lower.endswith(".tsv"):
            return OneLineTsvParser(config,filename)
        if lower.endswith(".json"):
            return JsonSectionParser(config,filename)
        raise ValueError(f"Unsupported file type: {filename}")
