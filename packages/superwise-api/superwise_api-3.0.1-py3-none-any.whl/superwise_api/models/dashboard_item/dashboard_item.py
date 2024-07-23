from datetime import datetime
from enum import Enum
from typing import Optional

from superwise_api.models import SuperwiseEntity
from superwise_api.models.dashboard.dashboard import VisualizationType
from superwise_api.models.dashboard.query import Query


class Datasource(str, Enum):
    DATASETS = "datasets"
    EVENTS = "events"


class QueryType(str, Enum):
    RAW_DATA = "raw_data"
    STATISTICS = "statistics"
    TIME_SERIES = "time_series"
    DISTRIBUTION = "distribution"


class DashboardItem(SuperwiseEntity):
    id: Optional[str]
    name: str
    query_type: Optional[QueryType]
    datasource: Optional[Datasource]
    visualization_type: Optional[VisualizationType]
    query: Optional[Query]
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    dashboard_id: Optional[str]
    item_metadata: Optional[dict[str, str]]

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[DashboardItem]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DashboardItem.parse_obj(obj)

        _obj = DashboardItem.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "query_type": QueryType(obj.get("query_type")),
                "datasource": Datasource(obj.get("datasource")),
                "query": Query.from_dict(obj.get("query")) if obj.get("query") is not None else None,
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "dashboard_id": obj.get("dashboard_id"),
                "item_metadata": obj.get("item_metadata"),
            }
        )
        return _obj
