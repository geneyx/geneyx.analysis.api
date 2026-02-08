from .IWarning import IWarning
from ..Models import JsonDict, FieldCondition, ConditionOperator

class ConditionWarning(IWarning):
    def format(self, config: JsonDict, data: JsonDict) -> str:
        # config["conditions"] is expected to be a list of FieldCondition-like dicts
        msgs = []
        for cond_dict in config.get("conditions", []):
            cond_dict["operator"] = ConditionOperator[cond_dict["operator"]]
            cond = FieldCondition(**cond_dict)
            if isinstance(data, dict):
                if cond_dict.get("field") in data:
                    data = data[cond_dict["field"]]
            warning = cond.__str__()
            if warning in msgs:
                continue
            if cond.check(data):
                msgs.append(warning)
                print(f"Warning triggered by condition: {warning}")
        return ". ".join(msgs)