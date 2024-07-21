from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from gscoordinator.flex.models.base_model import Model
from gscoordinator.flex.models.get_edge_type import GetEdgeType
from gscoordinator.flex.models.get_vertex_type import GetVertexType
from gscoordinator.flex import util

from gscoordinator.flex.models.get_edge_type import GetEdgeType  # noqa: E501
from gscoordinator.flex.models.get_vertex_type import GetVertexType  # noqa: E501

class GetGraphSchemaResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, vertex_types=None, edge_types=None):  # noqa: E501
        """GetGraphSchemaResponse - a model defined in OpenAPI

        :param vertex_types: The vertex_types of this GetGraphSchemaResponse.  # noqa: E501
        :type vertex_types: List[GetVertexType]
        :param edge_types: The edge_types of this GetGraphSchemaResponse.  # noqa: E501
        :type edge_types: List[GetEdgeType]
        """
        self.openapi_types = {
            'vertex_types': List[GetVertexType],
            'edge_types': List[GetEdgeType]
        }

        self.attribute_map = {
            'vertex_types': 'vertex_types',
            'edge_types': 'edge_types'
        }

        self._vertex_types = vertex_types
        self._edge_types = edge_types

    @classmethod
    def from_dict(cls, dikt) -> 'GetGraphSchemaResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetGraphSchemaResponse of this GetGraphSchemaResponse.  # noqa: E501
        :rtype: GetGraphSchemaResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def vertex_types(self) -> List[GetVertexType]:
        """Gets the vertex_types of this GetGraphSchemaResponse.


        :return: The vertex_types of this GetGraphSchemaResponse.
        :rtype: List[GetVertexType]
        """
        return self._vertex_types

    @vertex_types.setter
    def vertex_types(self, vertex_types: List[GetVertexType]):
        """Sets the vertex_types of this GetGraphSchemaResponse.


        :param vertex_types: The vertex_types of this GetGraphSchemaResponse.
        :type vertex_types: List[GetVertexType]
        """
        if vertex_types is None:
            raise ValueError("Invalid value for `vertex_types`, must not be `None`")  # noqa: E501

        self._vertex_types = vertex_types

    @property
    def edge_types(self) -> List[GetEdgeType]:
        """Gets the edge_types of this GetGraphSchemaResponse.


        :return: The edge_types of this GetGraphSchemaResponse.
        :rtype: List[GetEdgeType]
        """
        return self._edge_types

    @edge_types.setter
    def edge_types(self, edge_types: List[GetEdgeType]):
        """Sets the edge_types of this GetGraphSchemaResponse.


        :param edge_types: The edge_types of this GetGraphSchemaResponse.
        :type edge_types: List[GetEdgeType]
        """
        if edge_types is None:
            raise ValueError("Invalid value for `edge_types`, must not be `None`")  # noqa: E501

        self._edge_types = edge_types
