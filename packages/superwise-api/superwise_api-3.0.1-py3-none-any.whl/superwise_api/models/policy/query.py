from typing import Any
from typing import Optional
from typing import Union

from pydantic import BaseModel

from superwise_api.models import SuperwiseEntity


class PolicyQueryFilter(BaseModel):
    member: str
    operator: str
    values: Optional[Union[list[str], str]]


class PolicyQueryOrder(BaseModel):
    id: str
    desc: bool


class Query(SuperwiseEntity):
    measures: Optional[list[str]] = []
    order: Optional[Union[list[PolicyQueryOrder], PolicyQueryOrder]] = []
    dimensions: list[str] = []
    timezone: Optional[str] = "UTC"
    filters: list[PolicyQueryFilter] = []
    timeDimensions: Optional[list[dict[str, Any]]]
    limit: Optional[int]

    def to_dict(self):
        return self.dict(exclude_none=True)
