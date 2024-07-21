from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from gscoordinator.flex.models.base_model import Model
from gscoordinator.flex.models.primitive_type import PrimitiveType
from gscoordinator.flex.models.string_type import StringType
from gscoordinator.flex.models.string_type_string import StringTypeString
from gscoordinator.flex import util

from gscoordinator.flex.models.primitive_type import PrimitiveType  # noqa: E501
from gscoordinator.flex.models.string_type import StringType  # noqa: E501
from gscoordinator.flex.models.string_type_string import StringTypeString  # noqa: E501

class GSDataType(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, primitive_type=None, string=None):  # noqa: E501
        """GSDataType - a model defined in OpenAPI

        :param primitive_type: The primitive_type of this GSDataType.  # noqa: E501
        :type primitive_type: str
        :param string: The string of this GSDataType.  # noqa: E501
        :type string: StringTypeString
        """
        self.openapi_types = {
            'primitive_type': str,
            'string': StringTypeString
        }

        self.attribute_map = {
            'primitive_type': 'primitive_type',
            'string': 'string'
        }

        self._primitive_type = primitive_type
        self._string = string

    @classmethod
    def from_dict(cls, dikt) -> 'GSDataType':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GSDataType of this GSDataType.  # noqa: E501
        :rtype: GSDataType
        """
        return util.deserialize_model(dikt, cls)

    @property
    def primitive_type(self) -> str:
        """Gets the primitive_type of this GSDataType.


        :return: The primitive_type of this GSDataType.
        :rtype: str
        """
        return self._primitive_type

    @primitive_type.setter
    def primitive_type(self, primitive_type: str):
        """Sets the primitive_type of this GSDataType.


        :param primitive_type: The primitive_type of this GSDataType.
        :type primitive_type: str
        """
        allowed_values = ["DT_SIGNED_INT32", "DT_UNSIGNED_INT32", "DT_SIGNED_INT64", "DT_UNSIGNED_INT64", "DT_BOOL", "DT_FLOAT", "DT_DOUBLE"]  # noqa: E501
        if primitive_type not in allowed_values:
            raise ValueError(
                "Invalid value for `primitive_type` ({0}), must be one of {1}"
                .format(primitive_type, allowed_values)
            )

        self._primitive_type = primitive_type

    @property
    def string(self) -> StringTypeString:
        """Gets the string of this GSDataType.


        :return: The string of this GSDataType.
        :rtype: StringTypeString
        """
        return self._string

    @string.setter
    def string(self, string: StringTypeString):
        """Sets the string of this GSDataType.


        :param string: The string of this GSDataType.
        :type string: StringTypeString
        """
        if string is None:
            raise ValueError("Invalid value for `string`, must not be `None`")  # noqa: E501

        self._string = string
