import copy

import pytest
from drf_yasg import openapi

from drf_yasg_serializer_converter.swaggers_schema_properties.swagger_basic_responses import limited_list_response, \
    basic_get_responses, basic_post_responses, basic_put_responses, basic_patch_responses, basic_delete_responses
from .fixtures.conftest import *  # noqa: F401, F403

from tests.fixtures.serializers import HouseBasicSerializer, HouseOccupierSerializer, \
    HouseWithOccupiersSerializer, HouseOccupierWithBasicHouseSerializer
from .fixtures.openapi_responses import listed_house_occupier_response, listed_house_basic_response, \
    listed_house_with_occupiers_response, listed_house_occupier_with_basic_house_response, \
    basic_get_basic_house_response, basic_post_basic_house_response, basic_put_basic_house_response, \
    basic_patch_basic_house_response, basic_delete_basic_house_response
from .fixtures.openapi_schemas import house_basic_schema, house_occupier_schema, house_with_occupiers_schema, \
    house_occupier_with_basic_house_schema


def assert_generated_and_correct_schemas(generated_response: openapi.Response, correct_response: openapi.Response):
    assert dict(correct_response) == dict(generated_response)


@pytest.mark.parametrize("serializer, correct_response", [
    (HouseBasicSerializer, listed_house_basic_response),
    (HouseOccupierSerializer, listed_house_occupier_response),
    (HouseWithOccupiersSerializer, listed_house_with_occupiers_response),
    (HouseOccupierWithBasicHouseSerializer, listed_house_occupier_with_basic_house_response),
])
def test_generate_listed_serializer(serializer, correct_response):
    generated_schema = limited_list_response('', serializer)
    assert_generated_and_correct_schemas(generated_schema, correct_response)


@pytest.mark.parametrize("schema, correct_response", [
    (house_basic_schema, listed_house_basic_response),
    (house_occupier_schema, listed_house_occupier_response),
    (house_with_occupiers_schema, listed_house_with_occupiers_response),
    (house_occupier_with_basic_house_schema, listed_house_occupier_with_basic_house_response),
])
def test_generate_listed_schema(schema, correct_response):
    generated_schema = limited_list_response('', schema)
    assert_generated_and_correct_schemas(generated_schema, correct_response)


def test_custom_description():
    custom_description = "This is a custom description"
    generated_response = limited_list_response(custom_description, HouseBasicSerializer)
    correct_response = copy.deepcopy(listed_house_basic_response)
    correct_response.description = custom_description
    assert_generated_and_correct_schemas(generated_response, correct_response)


@pytest.mark.parametrize("basic_response_generator, correct_response", [
    (basic_get_responses, basic_get_basic_house_response),
    (basic_post_responses, basic_post_basic_house_response),
    (basic_put_responses, basic_put_basic_house_response),
    (basic_patch_responses, basic_patch_basic_house_response),
    (basic_delete_responses, basic_delete_basic_house_response),
])
def test_basic_responses_from_schema(basic_response_generator, correct_response):
    response_generated_from_schema = basic_response_generator(house_basic_schema)
    assert_generated_and_correct_schemas(response_generated_from_schema, correct_response)

    response_generated_from_serializer = basic_response_generator(HouseBasicSerializer)
    assert_generated_and_correct_schemas(response_generated_from_serializer, correct_response)
