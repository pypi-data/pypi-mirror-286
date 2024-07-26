from typing import Union

from drf_yasg import openapi
from drf_yasg.openapi import SchemaRef, Schema
from rest_framework.serializers import Serializer

from .openapi_schema_converters import get_schema


def limited_list_response(description: str,
                          object_schema: Union[Schema, SchemaRef, Serializer]) -> openapi.Response:
    obj_to_use = object_schema
    if not (isinstance(object_schema, Schema) or isinstance(object_schema, SchemaRef)):
        obj_to_use = get_schema(object_schema, '')
    collection_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'total': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Total number of objects without limiting.',
                example='100'
            ),
            'items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='List of returning items.',
                items=obj_to_use
            )
        }
    )
    return openapi.Response(description, collection_schema)


def basic_get_responses(data=None) -> dict:
    if not (isinstance(data, Schema) or isinstance(data, SchemaRef)):
        data = get_schema(data)
    return {
        200: data,
        404: openapi.Response('Object not found.')
    }


def basic_post_responses(data=None) -> dict:
    if not (isinstance(data, Schema) or isinstance(data, SchemaRef)):
        data = get_schema(data)
    return {
        201: data,
        400: openapi.Response('Bab request.')
    }


def basic_put_responses(data=None) -> dict:
    if not (isinstance(data, Schema) or isinstance(data, SchemaRef)):
        data = get_schema(data)
    return {
        200: data,
        404: openapi.Response('Object not found.')
    }


def basic_patch_responses(data=None) -> dict:
    if not (isinstance(data, Schema) or isinstance(data, SchemaRef)):
        data = get_schema(data)
    return {
        200: data,
        404: openapi.Response('Object not found.')
    }


def basic_delete_responses(data=None) -> dict:
    if not (isinstance(data, Schema) or isinstance(data, SchemaRef)):
        data = get_schema(data)
    return {
        204: data,
        404: openapi.Response('Object not found.')
    }


basic_delete_responses_without_object = {
    204: openapi.Response('Object deleted.'),
    404: openapi.Response('Object not found.')
}
