from typing import Any, Callable,Dict,Optional
from .ConditionOperator import ConditionOperator

class FieldCondition:
    def __init__(self, operator: ConditionOperator, value: Any, message: str, field: Optional[str] = None):
        self.operator = operator
        self.value = value
        self.message = message

    def check(self, value: Any) -> bool:
        func = OPERATOR_FUNCS[self.operator]
        return func(value, self.value)

    def __str__(self) -> str:
        return self.message

# map each operator to a function that compares (field_value, target_value) → bool
OPERATOR_FUNCS: Dict[ConditionOperator, Callable[[Any, Any], bool]] = {
    ConditionOperator.EQ:       lambda a, b: a == b,
    ConditionOperator.NE:       lambda a, b: a != b,
    ConditionOperator.GT:       lambda a, b: isinstance(a, (int, float)) and a > b,
    ConditionOperator.LT:       lambda a, b: isinstance(a, (int, float)) and a < b,
    ConditionOperator.GE:       lambda a, b: isinstance(a, (int, float)) and a >= b,
    ConditionOperator.LE:       lambda a, b: isinstance(a, (int, float)) and a <= b,
    ConditionOperator.CONTAINS: lambda a, b: (isinstance(a, str) and b in a)
                                or (isinstance(a, (list, set)) and b in a),
}


