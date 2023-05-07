from unittest.mock import patch, MagicMock

import pytest


from icecream_tubs.models import Flavor, IceCreamTub

pytestmark = pytest.mark.django_db


# --------------Test Flavors-------------- #
def test_create_flavor_should_succeed(flavor):
    assert flavor.id is not None
    assert str(flavor) == "CHOCOLATE_ORANGE"
    assert flavor.name == "CHOCOLATE_ORANGE"
    assert flavor.recipe == "Recipe description"


def test_save_should_set_the_corresponding_photo(flavor):
    assert flavor.photo.name == "flavor_photos/chocolate_orange.png"


def test_create_existing_flavor_name_should_fail(flavor):
    with pytest.raises(Exception):
        Flavor.objects.create(
            name="CHOCOLATE_ORANGE", recipe="Another Chocolate Orange recipe"
        )


# --------------Test IceCreamTub-------------- #


def test_create_icecream_tub_with_default_parameter_should_succeed(
    flavor, ice_cream_tub
):
    assert ice_cream_tub.id is not None
    assert str(ice_cream_tub) == "CHOCOLATE_ORANGE (40 scoops)"
    assert ice_cream_tub.flavor == flavor
    assert ice_cream_tub.scoops_available == 40


def test_create_icecream_tub_without_flavor_should_fail():
    with pytest.raises(Exception):
        IceCreamTub.objects.create()


@pytest.mark.parametrize("ice_cream_tub", [0], indirect=True)
def test_is_empty_when_scoops_available_is_zero_should_return_true(ice_cream_tub):
    assert ice_cream_tub.is_empty is True


@pytest.mark.parametrize("ice_cream_tub", [1], indirect=True)
def test_is_empty_when_scoops_available_is_positive_should_return_false(ice_cream_tub):
    assert ice_cream_tub.is_empty is False


@pytest.mark.parametrize("ice_cream_tub", [0], indirect=True)
def test_filling_rate_when_scoops_available_is_zero_should_return_zero(ice_cream_tub):
    assert ice_cream_tub.filling_rate == "0.0 %"


@pytest.mark.parametrize("ice_cream_tub", [20], indirect=True)
def test_filling_rate_when_scoops_available_is_halve_should_return_50(ice_cream_tub):
    assert ice_cream_tub.filling_rate == "50.0 %"


def test_filling_rate_when_scoops_available_full_should_return_100(ice_cream_tub):
    assert ice_cream_tub.filling_rate == "100.0 %"


@pytest.mark.parametrize("ice_cream_tub", [20], indirect=True)
def test_refill_tub_should_refill_tub_back_to_initial_stock(ice_cream_tub):
    ice_cream_tub.refill()
    assert ice_cream_tub.scoops_available == ice_cream_tub.scoops_initial_stock


@patch(
    "icecream_tubs.models.IceCreamTub.save",
    MagicMock(return_value="EMAIL: CHOCOLATE_ORANGE tub is empty"),
)
def test_save_empty_tub_should_send_email():
    flavor = Flavor.objects.create(
        name="CHOCOLATE_ORANGE", recipe="Chocolate Orange recipe"
    )
    ice_cream_tub = IceCreamTub(flavor=flavor, scoops_available=0)
    assert ice_cream_tub.save() == "EMAIL: CHOCOLATE_ORANGE tub is empty"
