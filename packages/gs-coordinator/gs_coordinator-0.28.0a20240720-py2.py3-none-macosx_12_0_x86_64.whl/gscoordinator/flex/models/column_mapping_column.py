from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from gscoordinator.flex.models.base_model import Model
from gscoordinator.flex import util


class ColumnMappingColumn(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, index=None, name=None):  # noqa: E501
        """ColumnMappingColumn - a model defined in OpenAPI

        :param index: The index of this ColumnMappingColumn.  # noqa: E501
        :type index: int
        :param name: The name of this ColumnMappingColumn.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'index': int,
            'name': str
        }

        self.attribute_map = {
            'index': 'index',
            'name': 'name'
        }

        self._index = index
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'ColumnMappingColumn':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ColumnMapping_column of this ColumnMappingColumn.  # noqa: E501
        :rtype: ColumnMappingColumn
        """
        return util.deserialize_model(dikt, cls)

    @property
    def index(self) -> int:
        """Gets the index of this ColumnMappingColumn.


        :return: The index of this ColumnMappingColumn.
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index: int):
        """Sets the index of this ColumnMappingColumn.


        :param index: The index of this ColumnMappingColumn.
        :type index: int
        """

        self._index = index

    @property
    def name(self) -> str:
        """Gets the name of this ColumnMappingColumn.


        :return: The name of this ColumnMappingColumn.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this ColumnMappingColumn.


        :param name: The name of this ColumnMappingColumn.
        :type name: str
        """

        self._name = name
