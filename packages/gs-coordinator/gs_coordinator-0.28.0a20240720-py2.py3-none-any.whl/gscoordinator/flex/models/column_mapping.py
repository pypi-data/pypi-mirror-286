from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from gscoordinator.flex.models.base_model import Model
from gscoordinator.flex.models.column_mapping_column import ColumnMappingColumn
from gscoordinator.flex import util

from gscoordinator.flex.models.column_mapping_column import ColumnMappingColumn  # noqa: E501

class ColumnMapping(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, column=None, _property=None):  # noqa: E501
        """ColumnMapping - a model defined in OpenAPI

        :param column: The column of this ColumnMapping.  # noqa: E501
        :type column: ColumnMappingColumn
        :param _property: The _property of this ColumnMapping.  # noqa: E501
        :type _property: str
        """
        self.openapi_types = {
            'column': ColumnMappingColumn,
            '_property': str
        }

        self.attribute_map = {
            'column': 'column',
            '_property': 'property'
        }

        self._column = column
        self.__property = _property

    @classmethod
    def from_dict(cls, dikt) -> 'ColumnMapping':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ColumnMapping of this ColumnMapping.  # noqa: E501
        :rtype: ColumnMapping
        """
        return util.deserialize_model(dikt, cls)

    @property
    def column(self) -> ColumnMappingColumn:
        """Gets the column of this ColumnMapping.


        :return: The column of this ColumnMapping.
        :rtype: ColumnMappingColumn
        """
        return self._column

    @column.setter
    def column(self, column: ColumnMappingColumn):
        """Sets the column of this ColumnMapping.


        :param column: The column of this ColumnMapping.
        :type column: ColumnMappingColumn
        """
        if column is None:
            raise ValueError("Invalid value for `column`, must not be `None`")  # noqa: E501

        self._column = column

    @property
    def _property(self) -> str:
        """Gets the _property of this ColumnMapping.

        must align with the schema  # noqa: E501

        :return: The _property of this ColumnMapping.
        :rtype: str
        """
        return self.__property

    @_property.setter
    def _property(self, _property: str):
        """Sets the _property of this ColumnMapping.

        must align with the schema  # noqa: E501

        :param _property: The _property of this ColumnMapping.
        :type _property: str
        """
        if _property is None:
            raise ValueError("Invalid value for `_property`, must not be `None`")  # noqa: E501

        self.__property = _property
