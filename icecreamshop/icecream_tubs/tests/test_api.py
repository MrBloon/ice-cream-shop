import json
import pytest
import os

from django.urls import reverse

from icecream_tubs.models import Flavor

flavors_url = reverse("flavors-list")
pytestmark = pytest.mark.django_db


# --------------Test Get Flavors-------------- #
def test_zero_flavors_should_return_empty_list(client) -> None:
    response = client.get(flavors_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_flavor_exists_should_succeed(client) -> None:
    test_flavor = Flavor.objects.create(
        name="CHOCOLATE_ORANGE",
        photo=None,
        recipe="Recipe description",
    )

    response = client.get(flavors_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_flavor.name
    assert os.path.basename(response_content.get("photo")) == os.path.basename(
        test_flavor.photo.name
    )
    assert response_content.get("recipe") == test_flavor.recipe


# --------------Test Post Flavors-------------- #
def test_create_flavor_without_arguments_should_fail(client) -> None:
    response = client.post(path=flavors_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["This field is required."],
        "recipe": ["This field is required."],
    }


def test_create_existing_flavor_name_should_fail(client) -> None:
    Flavor.objects.create(
        name="CHOCOLATE_ORANGE",
        photo=None,
        recipe="Recipe description",
    )
    response = client.post(
        path=flavors_url,
        data={"name": "CHOCOLATE_ORANGE", "photo": "", "recipe": "Recipe description"},
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["flavor with this name already exists."]
    }


def test_create_flavor_with_name_matching_photo_should_succeed(client) -> None:
    response = client.post(
        path=flavors_url,
        data={"name": "CHOCOLATE_ORANGE", "photo": "", "recipe": "Recipe description"},
    )
    assert response.status_code == 201
    response_content = response.json()
    assert response_content.get("name") == "CHOCOLATE_ORANGE"
    assert "chocolate_orange.png" in response_content.get("photo")
    assert response_content.get("recipe") == "Recipe description"
