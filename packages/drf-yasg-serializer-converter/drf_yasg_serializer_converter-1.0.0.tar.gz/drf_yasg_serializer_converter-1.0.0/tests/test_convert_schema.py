import copy

import pytest
from drf_yasg import openapi

from .fixtures.conftest import *  # noqa: F401, F403

from drf_yasg_serializer_converter.swaggers_schema_properties.openapi_schema_converters import get_schema
from tests.fixtures.serializers import HouseSerializer, HouseBasicSerializer, HouseOccupierSerializer, \
    HouseWithOccupiersSerializer, HouseOccupierWithHouseSerializer, HouseOccupierWithBasicHouseSerializer
from .fixtures.openapi_schemas import house_basic_schema, house_schema, house_occupier_schema, \
    house_with_occupiers_schema, house_occupier_with_house_schema, house_occupier_with_basic_house_schema


def assert_generated_and_correct_schemas(generated_schema: openapi.Schema, correct_schema: openapi.Schema):
    assert dict(correct_schema) == dict(generated_schema)


@pytest.mark.parametrize("serializer, correct_schema", [
    (HouseBasicSerializer, house_basic_schema), (HouseSerializer, house_schema),
    (HouseOccupierSerializer, house_occupier_schema),
    (HouseWithOccupiersSerializer, house_with_occupiers_schema),
    (HouseOccupierWithHouseSerializer, house_occupier_with_house_schema),
    (HouseOccupierWithBasicHouseSerializer, house_occupier_with_basic_house_schema),
])
def test_basic_convert(serializer, correct_schema):
    generated_schema = get_schema(serializer)
    assert_generated_and_correct_schemas(generated_schema, correct_schema)


def test_custom_description():
    custom_description = "This is a custom description"
    generated_schema = get_schema(HouseBasicSerializer, custom_description)
    correct_schema = copy.deepcopy(house_basic_schema)
    correct_schema.description = custom_description
    assert_generated_and_correct_schemas(generated_schema, correct_schema)
