from enum import Enum
class ConditionOperator(Enum):
    EQ         = "=="   # equality
    NE         = "!="   # not equal
    GT         = ">"    # greater than
    LT         = "<"    # less than
    GE         = ">="   # ≥
    LE         = "<="   # ≤
    CONTAINS   = "in"   # substring or membership
