import pytest
from django.db import IntegrityError

from orders.models import Order, OrderItem

pytestmark = pytest.mark.django_db


# --------------Test Order-------------- #
def test_create_order_with_default_parameter_should_succeed(order):
    assert order.id is not None
    assert str(order) == f"Order {order.order_number}: price (0 euros)"
    assert order.total_price == 0
    assert order.is_confirmed is False


def test_save_should_set_random_order_number(order):
    assert order.order_number is not None
    order.order_number = "123456789"
    order.save()
    assert order.order_number == "123456789"


def test_update_total_price_should_succeed(order):
    order.update_total_price(2, 2)
    assert order.total_price == 4


@pytest.mark.parametrize("order_item", [2], indirect=True)
def test_update_scoops_available_in_tubs_should_succeed(order_item):
    order_item.order.update_scoops_available_in_tubs()
    order_item.ice_cream_tub.refresh_from_db()

    assert (
        order_item.ice_cream_tub.scoops_available
        == order_item.ice_cream_tub.scoops_initial_stock - order_item.scoops_requested
    )


# --------------Test OrderItem-------------- #
def test_create_order_item_should_succeed(order, ice_cream_tub):
    order_item = OrderItem.objects.create(
        order=order, ice_cream_tub=ice_cream_tub, scoops_requested=2
    )
    assert order_item.id is not None
    assert order_item.order == order
    assert order_item.ice_cream_tub == ice_cream_tub
    assert order_item.scoops_requested == 2
    assert order.order_items.count() == 1
    assert str(order_item) == "CHOCOLATE_ORANGE - 2 scoops"


def test_create_order_item_with_invalid_scoops_requested_value_should_fail(
    ice_cream_tub, order
):
    with pytest.raises(IntegrityError):
        OrderItem.objects.create(
            ice_cream_tub=ice_cream_tub, scoops_requested=-2, order=order
        )


def test_create_order_item_without_order_should_fail(ice_cream_tub):
    with pytest.raises(IntegrityError):
        OrderItem.objects.create(ice_cream_tub=ice_cream_tub, scoops_requested=2)


def test_save_should_update_order_total_price(order, ice_cream_tub):
    assert order.total_price == 0
    order_item = OrderItem.objects.create(
        order=order, ice_cream_tub=ice_cream_tub, scoops_requested=2
    )
    assert order.total_price == 2 * order_item.price_per_scoop
