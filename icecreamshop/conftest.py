import pytest

from icecream_tubs.models import Flavor, IceCreamTub
from orders.models import Order, OrderItem


@pytest.fixture
def flavor():
    return Flavor.objects.create(name="CHOCOLATE_ORANGE", recipe="Recipe description")


@pytest.fixture
def ice_cream_tub(request, flavor):
    scoops_available = getattr(request, "param", 40)
    return IceCreamTub.objects.create(flavor=flavor, scoops_available=scoops_available)


@pytest.fixture
def order():
    return Order.objects.create(email="email@gmail.com")


@pytest.fixture
def order_item(request, order, ice_cream_tub):
    return OrderItem.objects.create(
        order=order, ice_cream_tub=ice_cream_tub, scoops_requested=request.param
    )
