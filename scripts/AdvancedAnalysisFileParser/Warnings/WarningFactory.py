from typing import Dict, Optional
from .IWarning import IWarning
from .CarrierPositiveWarning import CarrierPositiveWarning
from .GenotypeWarning import GenotypeWarning
from .ConditionWarning import ConditionWarning
from .SmnWarning import SmnWarning
from .GbaWarning import GbaWarning
class WarningFactory:
    @staticmethod
    def get_formatter(wtype: Optional[Dict]) -> IWarning:
        if wtype is None:
            raise ValueError("Warning type cannot be None")
        warning_type = None
        if isinstance(wtype, Dict) and "type" in wtype:
            warning_type = wtype["type"]
        if warning_type == None or warning_type == "":
            raise ValueError("Warning type cannot be empty")
        if warning_type == "condition":
            return ConditionWarning()
        if warning_type == "carrier_positive":
            return CarrierPositiveWarning()
        if warning_type == "genotype":
            return GenotypeWarning()
        if warning_type == "smn":
            return SmnWarning()
        if warning_type == "gba":
            return GbaWarning()
        if not isinstance(wtype, Dict):
            raise TypeError(f"Warning type must be a dict, got {type(wtype).__name__}")
        # If the warning type is not found, raise an error
        raise ValueError(f"Unknown warning type: {warning_type}")