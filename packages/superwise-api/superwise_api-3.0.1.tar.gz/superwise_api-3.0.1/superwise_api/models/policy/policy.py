from datetime import datetime
from enum import Enum
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveFloat
from pydantic import PositiveInt

from superwise_api.models import SuperwiseEntity
from superwise_api.models.policy.query import Query


class ThresholdTypes(str, Enum):
    STATIC: Literal["static"] = "static"
    MOVING_AVERAGE: Literal["moving_average"] = "moving_average"


class ThresholdSettings(BaseModel):
    threshold_type: Literal["static", "moving_average"] = Field(...)

    def to_dict(self) -> dict:
        return self.dict(exclude_none=True)


class StaticThresholdSettings(ThresholdSettings):
    condition_above_value: Optional[float]
    condition_below_value: Optional[float]
    threshold_type: Literal["static"] = ThresholdTypes.STATIC.value


class MovingAverageThresholdSettings(ThresholdSettings):
    is_violation_above: bool = True
    is_violation_below: bool = True
    violation_deviation: PositiveFloat
    threshold_type: Literal["moving_average"] = ThresholdTypes.MOVING_AVERAGE.value
    window_size: PositiveInt


class AlertOnStatusDirection(str, Enum):
    HEALTHY_TO_UNHEALTHY = "HEALTHY_TO_UNHEALTHY"
    UNHEALTHY_TO_HEALTHY = "UNHEALTHY_TO_HEALTHY"
    BOTH = "BOTH"


class TimeRangeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class Policy(SuperwiseEntity):
    id: str
    name: str
    query: Query
    cron_expression: str
    threshold_settings: Union[StaticThresholdSettings, MovingAverageThresholdSettings] = Field(
        discriminator="threshold_type"
    )
    alert_on_status: AlertOnStatusDirection
    alert_on_policy_level: bool
    dataset_id: str
    destination_ids: list[str]
    time_range_field: str
    time_range_unit: TimeRangeUnit
    time_range_value: int
    last_evaluation: Optional[datetime]
    next_evaluation: Optional[datetime]
    status: Optional[str]
    status_reason: Optional[dict] = None
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    tenant_id: str

    def to_dict(self) -> dict:
        dict_ = self.dict(exclude_none=True)
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict) -> "Policy":
        dict_["query"] = Query(**dict_["query"])
        if dict_["threshold_settings"]["threshold_type"] == ThresholdTypes.STATIC.value:
            dict_["threshold_settings"] = StaticThresholdSettings(**dict_["threshold_settings"])
        else:
            dict_["threshold_settings"] = MovingAverageThresholdSettings(**dict_["threshold_settings"])
        return cls(**dict_)
