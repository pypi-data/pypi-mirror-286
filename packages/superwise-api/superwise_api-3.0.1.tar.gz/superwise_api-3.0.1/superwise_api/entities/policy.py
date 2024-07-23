from typing import Optional
from typing import Union

from superwise_api.client.models.page import Page
from superwise_api.entities.base import BaseApi
from superwise_api.models.policy.policy import AlertOnStatusDirection
from superwise_api.models.policy.policy import MovingAverageThresholdSettings
from superwise_api.models.policy.policy import Policy
from superwise_api.models.policy.policy import Query
from superwise_api.models.policy.policy import StaticThresholdSettings
from superwise_api.models.policy.policy import TimeRangeUnit


class PolicyApi(BaseApi):
    _model_name = "policy"
    _resource_path = "/v1/policies"
    _model_class = Policy

    def create(
        self,
        name: str,
        query: Query,
        cron_expression: str,
        threshold_settings: Union[StaticThresholdSettings, MovingAverageThresholdSettings],
        alert_on_status: AlertOnStatusDirection,
        alert_on_policy_level: bool,
        dataset_id: str,
        destination_ids: list[str],
        time_range_field: str,
        time_range_unit: TimeRangeUnit,
        time_range_value: int,
        **kwargs,
    ) -> Policy:
        """
        Create a new policy

        Args:
            name: The name of the policy
            query: The query object that defines the data to be monitored
            cron_expression: The cron expression that defines the schedule of the policy
            threshold_settings: The threshold settings for the policy
            alert_on_status: The direction of the alert
            alert_on_policy_level: Whether to alert on policy level
            dataset_id: The dataset id
            destination_ids: The destination ids
            time_range_field: The time range field
            time_range_unit: The time range unit
            time_range_value: The time range value
            **kwargs: Arbitrary keyword arguments

        Returns:
            The created policy
        """
        data = {
            k: v
            for k, v in dict(
                name=name,
                query=query,
                cron_expression=cron_expression,
                threshold_settings=threshold_settings,
                alert_on_status=alert_on_status,
                alert_on_policy_level=alert_on_policy_level,
                dataset_id=dataset_id,
                destination_ids=destination_ids,
                time_range_field=time_range_field,
                time_range_unit=time_range_unit,
                time_range_value=time_range_value,
            ).items()
            if v is not None
        }
        return self.api_client.create(
            resource_path=self._resource_path, model_name=self._model_name, model_class=Policy, data=data, **kwargs
        )

    def get_by_id(self, policy_id: str, **kwargs) -> Policy:
        """
        Gets a policy by id.

        Args:
            policy_id (str): The id of the policy.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Policy: The retrieved policy.
        """
        return super().get_by_id(_id=policy_id, **kwargs)

    def get(
        self,
        name: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        dataset_id: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **kwargs,
    ) -> Page:
        """
        Gets policies. Filter if any of the parameters are provided.

        Args:
            name (str, optional): The name of the policy.
            status (str, optional): The status of the policy.
            created_by (str, optional): The creator of the policy.
            dataset_id (str, optional): The id of the dataset.
            page (int, optional): The page number.
            size (int, optional): The size of the page.
            **kwargs: Arbitrary keyword arguments

        Returns:
            Page: A page of policies.
        """
        query_params = {
            k: v
            for k, v in dict(
                name=name, status=status, created_by=created_by, dataset_id=dataset_id, page=page, size=size
            ).items()
            if v is not None
        }
        return self.api_client.get(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=Policy,
            query_params=query_params,
            **kwargs,
        )

    def update(
        self,
        policy_id: str,
        *,
        name: Optional[str] = None,
        query: Optional[Query] = None,
        cron_expression: Optional[str] = None,
        destination_ids: Optional[list[str]] = None,
        alert_on_status: Optional[AlertOnStatusDirection] = None,
        alert_on_policy_level: Optional[bool] = None,
        dataset_id: Optional[str] = None,
        time_range_field: Optional[str] = None,
        time_range_unit: Optional[TimeRangeUnit] = None,
        time_range_value: Optional[int] = None,
        threshold_settings: Optional[Union[StaticThresholdSettings, MovingAverageThresholdSettings]] = None,
        **kwargs,
    ) -> Policy:
        """
        Update a policy.

        Args:
            policy_id: The id of the policy
            name: The name of the policy
            query: The query object that defines the data to be monitored
            cron_expression: The cron expression that defines the schedule of the policy
            threshold_settings: The threshold settings for the policy
            alert_on_status: The direction of the alert
            alert_on_policy_level: Whether to alert on policy level
            dataset_id: The dataset id
            destination_ids: The destination ids
            time_range_field: The time range field
            time_range_unit: The time range unit
            time_range_value: The time range value
            **kwargs: Arbitrary keyword arguments

        Returns:
            The updated policy.
        """
        if not any(
            [
                name,
                query,
                cron_expression,
                threshold_settings,
                alert_on_status,
                alert_on_policy_level,
                dataset_id,
                destination_ids,
                time_range_field,
                time_range_unit,
                time_range_value,
            ]
        ):
            raise ValueError("At least one parameter must be provided to update the policy.")

        data = {
            k: v
            for k, v in dict(
                name=name,
                query=query,
                cron_expression=cron_expression,
                destination_ids=destination_ids,
                alert_on_status=alert_on_status,
                alert_on_policy_level=alert_on_policy_level,
                dataset_id=dataset_id,
                time_range_field=time_range_field,
                time_range_unit=time_range_unit,
                time_range_value=time_range_value,
                threshold_settings=threshold_settings,
            ).items()
            if v is not None
        }
        return self.api_client.update(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=Policy,
            entity_id=policy_id,
            data=data,
            **kwargs,
        )

    def delete(self, policy_id: str, **kwargs):
        """
        Deletes a policy.

        Args:
            policy_id (str): The id of the policy to delete.
            **kwargs: Arbitrary keyword arguments
        """
        return super().delete(_id=policy_id, **kwargs)

    @BaseApi.raise_exception
    def trigger(self, policy_id: str, **kwargs):
        """
        Trigger a policy.

        Args:
            policy_id (str): The id of the policy to trigger.
            **kwargs: Arbitrary keyword arguments.
        """
        return self.api_client.post(
            resource_path=f"{self._resource_path}/{policy_id}/trigger",
            **kwargs,
        )
