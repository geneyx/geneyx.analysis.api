from .IWarning import IWarning
from ..Models import *
class CarrierPositiveWarning(IWarning):
    def format(self, config: JsonDict, data: JsonDict) -> str:
        name = config.get("caller_name") or config.get("name")
        disease = config.get("disease_name") or config.get("disease")
        conditions = config.get("conditions",{})
        for condition in conditions:
            condition["operator"] = ConditionOperator[condition["operator"]]
            field_condition = FieldCondition(
                field= condition.get("field",None),
                operator=condition.get("operator"),
                value=condition.get("value"),
                message=f"Based on the {name}, this sample is <b>Positive</b> for {disease}"
            )
            if field_condition.check(data):
                return field_condition.__str__()
        return ""