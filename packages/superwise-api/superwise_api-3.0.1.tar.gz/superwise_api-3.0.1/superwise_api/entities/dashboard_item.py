from typing import Optional

from pydantic import conint

from superwise_api.client.models.page import Page
from superwise_api.entities.base import BaseApi
from superwise_api.models.dashboard.dashboard import VisualizationType
from superwise_api.models.dashboard.query import Query
from superwise_api.models.dashboard_item.dashboard_item import DashboardItem
from superwise_api.models.dashboard_item.dashboard_item import Datasource
from superwise_api.models.dashboard_item.dashboard_item import QueryType


class DashboardItemApi(BaseApi):
    """
    This class provides methods to interact with the DashboardItem API.

    Args:
        api_client (SuperwiseClient): An instance of the ApiClient to make requests.
    """

    _model_name = "dashboard_item"
    _resource_path = "/v1/dashboard-items"
    _model_class = DashboardItem

    def get_by_id(self, dashboard_item_id: str, **kwargs) -> DashboardItem:
        """
        Gets a dashboard_item by id.

        Args:
            dashboard_item_id (str): The id of the dashboard_item.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DashboardItem: The dashboard_item.
        """
        return super().get_by_id(_id=dashboard_item_id, **kwargs)

    def delete(self, dashboard_item_id: str, **kwargs) -> None:
        """
        Deletes a dashboard_item.

        Args:
            dashboard_item_id (str): The id of the dashboard_item.
            **kwargs: Arbitrary keyword arguments.
        """
        return super().delete(_id=dashboard_item_id, **kwargs)

    def create(
        self,
        name: str,
        query_type: QueryType,
        visualization_type: VisualizationType,
        datasource: Datasource,
        query: Query,
        dashboard_id: str,
        item_metadata: dict,
        **kwargs
    ) -> DashboardItem:
        """
        Creates a new dashboard_item.

        Args:
            name (str): The name of the dashboard_item.
            query_type (QueryType): The type of query this dashboard item will execute.
            visualization_type (VisualizationType): The type of visualization to be used for this item.
            datasource (Datasource): Identifier for the data source from which this item retrieves data.
            query (Query): The actual query to be executed by this dashboard item.
            dashboard_id (str): The ID of the dashboard to which this item belongs.
            item_metadata (dict, optional): Additional metadata for the item, such as visual settings.
            **kwargs: Arbitrary keyword arguments for future extensions or additional data.

        Returns:
            DashboardItem: The created dashboard_item.
        """
        data = {
            "name": name,
            "query_type": query_type,
            "visualization_type": visualization_type,
            "datasource": datasource,
            "query": query,
            "dashboard_id": dashboard_id,
            "item_metadata": item_metadata,
        }

        return self.api_client.create(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=DashboardItem,
            data=data,
            **kwargs,
        )

    def get(
        self,
        name: Optional[str] = None,
        dashboard_id: Optional[str] = None,
        page: Optional[conint(strict=True, ge=1)] = None,
        size: Optional[conint(strict=True, le=500, ge=1)] = None,
        **kwargs
    ) -> Page:
        """
        Gets all dashboard_items.

        Args:
            name (str, optional): The name of the dashboard_item.
            dashboard_id (str, optional): The id of the dashboard.
            page (int, optional): The page number.
            size (int, optional): The size of the page.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of sources.
        """
        query_params = {
            k: v for k, v in dict(name=name, dashboard_id=dashboard_id, page=page, size=size).items() if v is not None
        }
        return self.api_client.get(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=DashboardItem,
            query_params=query_params,
            **kwargs,
        )

    def update(
        self,
        dashboard_item_id: str,
        *,
        name: Optional[str] = None,
        query_type: Optional[QueryType] = None,
        visualization_type: Optional[VisualizationType] = None,
        datasource: Optional[Datasource] = None,
        query: Optional[Query] = None,
        item_metadata: Optional[dict] = None,
        **kwargs
    ) -> DashboardItem:
        """
        Updates a dashboard item.

        Args:
            dashboard_item_id (str): The unique identifier of the dashboard item.
            name (str, optional): New name of the dashboard item.
            query_type (QueryType, optional): New type of query to be executed.
            visualization_type (VisualizationType, optional): New visualization type to be used.
            datasource (Datasource, optional): New data source identifier.
            query (Query, optional): New query definition.
            item_metadata (dict, optional): New additional metadata for the item.
            **kwargs: Arbitrary keyword arguments for future extensions or additional data.

        Returns:
            DashboardItem: The updated dashboard item.
        """
        if not any([name, query_type, visualization_type, datasource, query, item_metadata]):
            raise ValueError("At least one parameter must be provided to update the dashboard item.")

        data = {
            "name": name,
            "query_type": query_type,
            "datasource": datasource,
            "query": query,
            "visualization_type": visualization_type,
            "item_metadata": item_metadata,
        }
        # Remove None values to ensure only provided fields are updated
        data = {k: v for k, v in data.items() if v is not None}
        data.update(kwargs)  # Include any additional arbitrary keyword arguments

        return self.api_client.update(
            resource_path=self._resource_path,
            entity_id=dashboard_item_id,
            model_name=self._model_name,
            model_class=DashboardItem,
            data=data,
            **kwargs,
        )
