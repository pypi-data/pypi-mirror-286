from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from gscoordinator.flex.models.base_model import Model
from gscoordinator.flex import util


class GetAlertMessageResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, alert_name=None, severity=None, metric_type=None, target=None, trigger_time=None, status=None, message=None):  # noqa: E501
        """GetAlertMessageResponse - a model defined in OpenAPI

        :param id: The id of this GetAlertMessageResponse.  # noqa: E501
        :type id: str
        :param alert_name: The alert_name of this GetAlertMessageResponse.  # noqa: E501
        :type alert_name: str
        :param severity: The severity of this GetAlertMessageResponse.  # noqa: E501
        :type severity: str
        :param metric_type: The metric_type of this GetAlertMessageResponse.  # noqa: E501
        :type metric_type: str
        :param target: The target of this GetAlertMessageResponse.  # noqa: E501
        :type target: List[str]
        :param trigger_time: The trigger_time of this GetAlertMessageResponse.  # noqa: E501
        :type trigger_time: str
        :param status: The status of this GetAlertMessageResponse.  # noqa: E501
        :type status: str
        :param message: The message of this GetAlertMessageResponse.  # noqa: E501
        :type message: str
        """
        self.openapi_types = {
            'id': str,
            'alert_name': str,
            'severity': str,
            'metric_type': str,
            'target': List[str],
            'trigger_time': str,
            'status': str,
            'message': str
        }

        self.attribute_map = {
            'id': 'id',
            'alert_name': 'alert_name',
            'severity': 'severity',
            'metric_type': 'metric_type',
            'target': 'target',
            'trigger_time': 'trigger_time',
            'status': 'status',
            'message': 'message'
        }

        self._id = id
        self._alert_name = alert_name
        self._severity = severity
        self._metric_type = metric_type
        self._target = target
        self._trigger_time = trigger_time
        self._status = status
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'GetAlertMessageResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetAlertMessageResponse of this GetAlertMessageResponse.  # noqa: E501
        :rtype: GetAlertMessageResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this GetAlertMessageResponse.

        Generated in server side  # noqa: E501

        :return: The id of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this GetAlertMessageResponse.

        Generated in server side  # noqa: E501

        :param id: The id of this GetAlertMessageResponse.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def alert_name(self) -> str:
        """Gets the alert_name of this GetAlertMessageResponse.


        :return: The alert_name of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._alert_name

    @alert_name.setter
    def alert_name(self, alert_name: str):
        """Sets the alert_name of this GetAlertMessageResponse.


        :param alert_name: The alert_name of this GetAlertMessageResponse.
        :type alert_name: str
        """
        if alert_name is None:
            raise ValueError("Invalid value for `alert_name`, must not be `None`")  # noqa: E501

        self._alert_name = alert_name

    @property
    def severity(self) -> str:
        """Gets the severity of this GetAlertMessageResponse.


        :return: The severity of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity: str):
        """Sets the severity of this GetAlertMessageResponse.


        :param severity: The severity of this GetAlertMessageResponse.
        :type severity: str
        """
        allowed_values = ["warning", "emergency"]  # noqa: E501
        if severity not in allowed_values:
            raise ValueError(
                "Invalid value for `severity` ({0}), must be one of {1}"
                .format(severity, allowed_values)
            )

        self._severity = severity

    @property
    def metric_type(self) -> str:
        """Gets the metric_type of this GetAlertMessageResponse.


        :return: The metric_type of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._metric_type

    @metric_type.setter
    def metric_type(self, metric_type: str):
        """Sets the metric_type of this GetAlertMessageResponse.


        :param metric_type: The metric_type of this GetAlertMessageResponse.
        :type metric_type: str
        """
        allowed_values = ["node", "service"]  # noqa: E501
        if metric_type not in allowed_values:
            raise ValueError(
                "Invalid value for `metric_type` ({0}), must be one of {1}"
                .format(metric_type, allowed_values)
            )

        self._metric_type = metric_type

    @property
    def target(self) -> List[str]:
        """Gets the target of this GetAlertMessageResponse.


        :return: The target of this GetAlertMessageResponse.
        :rtype: List[str]
        """
        return self._target

    @target.setter
    def target(self, target: List[str]):
        """Sets the target of this GetAlertMessageResponse.


        :param target: The target of this GetAlertMessageResponse.
        :type target: List[str]
        """
        if target is None:
            raise ValueError("Invalid value for `target`, must not be `None`")  # noqa: E501

        self._target = target

    @property
    def trigger_time(self) -> str:
        """Gets the trigger_time of this GetAlertMessageResponse.


        :return: The trigger_time of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._trigger_time

    @trigger_time.setter
    def trigger_time(self, trigger_time: str):
        """Sets the trigger_time of this GetAlertMessageResponse.


        :param trigger_time: The trigger_time of this GetAlertMessageResponse.
        :type trigger_time: str
        """
        if trigger_time is None:
            raise ValueError("Invalid value for `trigger_time`, must not be `None`")  # noqa: E501

        self._trigger_time = trigger_time

    @property
    def status(self) -> str:
        """Gets the status of this GetAlertMessageResponse.


        :return: The status of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this GetAlertMessageResponse.


        :param status: The status of this GetAlertMessageResponse.
        :type status: str
        """
        allowed_values = ["unsolved", "solved", "dealing"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def message(self) -> str:
        """Gets the message of this GetAlertMessageResponse.


        :return: The message of this GetAlertMessageResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this GetAlertMessageResponse.


        :param message: The message of this GetAlertMessageResponse.
        :type message: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message
