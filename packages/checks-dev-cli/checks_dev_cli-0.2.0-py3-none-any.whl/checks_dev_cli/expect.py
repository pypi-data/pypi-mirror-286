
from enum import Enum

from pydantic import BaseModel, ConfigDict


class Operator(str, Enum):
    contains = "contains"
    equals = "equals"
    greater_than = "greaterThan"
    less_than = "lessThan"
    not_contains = "notContains"
    not_equals = "notEquals"


class BaseExpect(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    type: str
    # Make operator an enum of valid operators
    operator: Operator
    value: int|str