import json
import pytest


from django.urls import reverse


flavors_list_url = reverse("flavors-list")
icecream_tubs_list_url = reverse("icecream_tubs-list")
pytestmark = pytest.mark.django_db


# --------------Test Get Flavor-------------- #
def test_list_zero_flavors_should_return_empty_list(client) -> None:
    response = client.get(flavors_list_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_list_one_flavor_should_return_a_one_element_list(client, flavor) -> None:
    response = client.get(flavors_list_url)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


# --------------Test Post Flavor-------------- #
def test_create_flavor_should_succeed(client) -> None:
    response = client.post(
        path=flavors_list_url,
        data={"name": "CHOCOLATE_ORANGE", "photo": "", "recipe": "Recipe description"},
    )
    assert response.status_code == 201
    assert json.loads(response.content) == {
        "id": 1,
        "name": "CHOCOLATE_ORANGE",
        "photo": "http://testserver/media/flavor_photos/chocolate_orange.png",
        "recipe": "Recipe description",
    }


def test_create_flavor_without_arguments_should_fail(client) -> None:
    response = client.post(path=flavors_list_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["This field is required."],
        "recipe": ["This field is required."],
    }


def test_create_existing_flavor_name_should_fail(client, flavor) -> None:
    response = client.post(
        path=flavors_list_url,
        data={"name": "CHOCOLATE_ORANGE", "photo": "", "recipe": "Recipe description"},
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["flavor with this name already exists."]
    }


# --------------Test Get IceCreamTub-------------- #
def test_list_zero_icecream_tub_should_return_empty_list(client) -> None:
    response = client.get(icecream_tubs_list_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_list_one_icecream_tub_should_return_a_one_element_list(
    client, ice_cream_tub
) -> None:
    response = client.get(icecream_tubs_list_url)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


# --------------Test Post IceCreamTub-------------- #
def test_create_icecream_tub_should_succeed(client, flavor) -> None:
    response = client.post(
        path=icecream_tubs_list_url,
        data={"flavor": flavor.id},
    )
    assert response.status_code == 201
    assert json.loads(response.content) == {
        "id": 1,
        "scoops_available": 40,
        "flavor": 1,
    }


def test_create_existing_icecream_tub_should_fail(client, ice_cream_tub) -> None:
    response = client.post(
        path=icecream_tubs_list_url,
        data={"flavor": ice_cream_tub.flavor.id},
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "flavor": ["ice cream tub with this flavor already exists."]
    }
