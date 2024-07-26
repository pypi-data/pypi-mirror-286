import inspect
from typing import Dict, List, Tuple

from django.db import models
from drf_yasg import openapi
from rest_framework.serializers import Serializer, BaseSerializer

rest_framework_openapi_field_mapping = {
    "ListField": openapi.TYPE_ARRAY,
    "CharField": openapi.TYPE_STRING,
    "BooleanField": openapi.TYPE_BOOLEAN,
    "FloatField": openapi.TYPE_NUMBER,
    "DateTimeField": openapi.TYPE_STRING,
    "DateField": openapi.TYPE_STRING,
    "IntegerField": openapi.TYPE_INTEGER,
    "SerializerMethodField": openapi.TYPE_STRING
}

additional_info_fields_conversions = {
    "read_only": "readOnly",
    "allow_null": "x-nullable",
    "max_value": "maximum",
    "min_value": "minimum",
    "max_length": "maxLength",
    "min_length": "minLength",
}


def _get_additional_properties(field, serializer_meta_model_field: models.Field) -> Dict:
    additional_properties = {}
    dict_field = field.__dict__
    if serializer_meta_model_field is not None:
        if serializer_meta_model_field.default != models.fields.NOT_PROVIDED:
            additional_properties['default'] = serializer_meta_model_field.default
        if serializer_meta_model_field.blank and serializer_meta_model_field.null:
            additional_properties['x-nullable'] = serializer_meta_model_field.blank
    for field_property, final_property in additional_info_fields_conversions.items():
        if dict_field.get(field_property):
            additional_properties[final_property] = dict_field[field_property]
    return additional_properties


def _get_required(field: str) -> bool:
    if "required=False" not in field:
        return True
    else:
        return False


def _get_field_description(field: str) -> str | None:
    if "help_text=" in field:
        return field.split("help_text='")[-1].split("'")[0]


def _get_serializer_description(serializer: Serializer | BaseSerializer) -> str | None:
    if hasattr(serializer, 'openapi_help_text') and serializer.openapi_help_text:
        return serializer.openapi_help_text


def _specify_field_format(rest_framework_field_type: str, additional_properties: Dict):
    if additional_properties.get("format") is None:
        if rest_framework_field_type == "DateTimeField":
            additional_properties['format'] = 'date-time'
        if rest_framework_field_type == "DateField":
            additional_properties['format'] = 'date'


def _parse_rest_framework_field(field, serializer_meta_model_field: models.Field) -> Tuple[bool, openapi.Schema]:
    additional_properties = _get_additional_properties(field, serializer_meta_model_field)
    field_str = str(field)
    rest_framework_field_type = field_str.split("(")[0]
    openapi_field_type = rest_framework_openapi_field_mapping.get(rest_framework_field_type, openapi.TYPE_STRING)
    _specify_field_format(rest_framework_field_type, additional_properties)
    field_description = _get_field_description(field_str)
    field_required = _get_required(field_str)
    return field_required, openapi.Schema(type=openapi_field_type,
                                          description=field_description,
                                          **additional_properties)


def _parse_serializer(serializer: Serializer) -> Tuple[Dict[str, openapi.Schema], List[str]]:
    properties = {}
    field_description = ''
    required_properties = []
    # checking if there is any chance to get NestedSerializer from non default Serializer
    if (isinstance(serializer, BaseSerializer) and not isinstance(serializer, Serializer)) \
            and hasattr(serializer, 'child') and isinstance(serializer.child, Serializer):
        serializer = serializer.child
    # trying to get Model from Serializer
    serializer_class = type(serializer)
    serializer_meta_model = None
    if hasattr(serializer_class, 'Meta') and hasattr(serializer_class.Meta, 'model'):
        serializer_meta_model = serializer_class.Meta.model
    # parsing fields
    for k, v in serializer.get_fields().items():
        serializer_meta_model_field = None
        if serializer_meta_model is not None:
            serializer_meta_model_field = getattr(serializer_meta_model, k).field
        if v.__module__ == "rest_framework.fields":
            property_required, properties[k] = _parse_rest_framework_field(v, serializer_meta_model_field)
            if property_required:
                required_properties.append(k)
        elif isinstance(v, BaseSerializer):
            object_properties, object_required_properties = _parse_serializer(v)
            additional_properties = _get_additional_properties(v, serializer_meta_model_field)
            if _get_serializer_description(v):  # openapi_help_text - reserved name for this convertor
                field_description = _get_serializer_description(v)
            if _get_required(str(v)):
                required_properties.append(k)
            property_schema = openapi.Schema(type=openapi.TYPE_OBJECT,
                                             description=field_description,
                                             properties=object_properties,
                                             required=object_required_properties,
                                             **additional_properties)
            if hasattr(v, 'many') and v.many is not None and v.many:
                property_schema = openapi.Schema(type=openapi.TYPE_ARRAY,
                                                 items=property_schema)
            properties[k] = property_schema
        else:
            pass
    return properties, required_properties


def get_schema(serializer: Serializer, description: str = '') -> openapi.Schema:
    """ Converts object of type Serializer or inherited from Serializer class to an openapi.Schema object. """
    if inspect.isclass(serializer) and issubclass(serializer, Serializer):
        serializer = serializer()
    properties, required_properties = _parse_serializer(serializer)
    if _get_serializer_description(serializer):  # openapi_help_text - reserved name for this convertor
        description = _get_serializer_description(serializer)
    return_openapi_schema = openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties,
                                           description=description, required=required_properties)
    return return_openapi_schema
