import json

import pytest


from django.urls import reverse


orders_list_url = reverse("orders-list")
order_detail_url = reverse("orders-detail", args=[1])
order_confirm_url = reverse("orders-confirm", args=[1])
order_items_list_url = reverse("order_items-list", args=[1])
order_item_detail_url = reverse("order_items-detail", args=[1, 1])
pytestmark = pytest.mark.django_db
EMAIL_ADDRESS = "email@gmail.com"


# --------------Test Get Order-------------- #
def test_list_zero_orders_should_return_empty_list(client) -> None:
    response = client.get(orders_list_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_list_one_order_should_return_a_one_element_list(client, order) -> None:
    response = client.get(orders_list_url)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


def test_retrieve_order_should_succeed(client, order) -> None:
    response = client.get(order_detail_url)
    assert response.status_code == 200
    response_data = json.loads(response.content)
    del response_data["order_number"]
    assert response_data == {
        "id": 1,
        "order_items": [],
        "email": EMAIL_ADDRESS,
        "total_price": "0.00",
        "is_confirmed": False,
    }


def test_retrieve_non_existent_order_should_not_be_found(client) -> None:
    response = client.get(order_detail_url)
    assert response.status_code == 404
    assert json.loads(response.content) == {"detail": "Not found."}


# --------------Test Post Order-------------- #
def test_create_order_with_default_should_succeed(client) -> None:
    response = client.post(path=orders_list_url, data={"email": EMAIL_ADDRESS})
    assert response.status_code == 201
    response_data = json.loads(response.content)
    del response_data["order_number"]
    assert response_data == {
        "id": 1,
        "order_items": [],
        "email": EMAIL_ADDRESS,
        "total_price": "0.00",
        "is_confirmed": False,
    }


def test_create_order_without_email_should_fail(client) -> None:
    response = client.post(path=orders_list_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"email": ["This field is required."]}


# --------------Test Patch Order-------------- #
@pytest.mark.parametrize("order_item", [2], indirect=True)
def test_confirm_order_should_update_the_is_confirmed_attribute(
    client, order_item
) -> None:
    response = client.patch(order_confirm_url)
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["is_confirmed"] == True


@pytest.mark.parametrize("order_item", [2], indirect=True)
def test_confirm_order_should_update_scoops_available_in_tubs(
    client, order_item
) -> None:
    tub = order_item.ice_cream_tub
    assert tub.scoops_available == 40
    response = client.patch(order_confirm_url)
    assert response.status_code == 200
    tub.refresh_from_db()
    expected_scoops_available = tub.scoops_initial_stock - order_item.scoops_requested
    assert tub.scoops_available == expected_scoops_available


def test_confirm_order_without_order_items_should_fail(client, order) -> None:
    response = client.patch(order_confirm_url)
    assert response.status_code == 400
    assert json.loads(response.content) == [
        "To confirm the order, add at least one item."
    ]


# --------------Test Get OrderItem-------------- #
def test_list_zero_order_items_should_return_empty_list(client, order) -> None:
    response = client.get(order_items_list_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.parametrize("order_item", [2], indirect=True)
def test_list_one_order_item_should_return_a_one_element_list(
    client, order_item
) -> None:
    response = client.get(order_items_list_url)
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


@pytest.mark.parametrize("order_item", [2], indirect=True)
def test_list_order_items_should_return_only_order_items_from_the_order(
    client, order_item
) -> None:
    response = client.get(order_items_list_url)
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert len(response_data) == 1
    assert response_data[0]["order"] == order_item.order.id


@pytest.mark.parametrize("order_item", [2], indirect=True)
def test_retrieve_order_item_should_succeed(client, order_item) -> None:
    response = client.get(order_item_detail_url)
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {
        "id": 1,
        "order": 1,
        "ice_cream_tub": 1,
        "scoops_requested": 2,
    }


def test_retrieve_existent_order_item_should_not_be_found(client, order) -> None:
    response = client.get(order_item_detail_url)
    assert response.status_code == 404
    assert json.loads(response.content) == {"detail": "Not found."}


# --------------Test Post OrderItem-------------- #
def test_create_order_item_should_succeed(client, order, ice_cream_tub) -> None:
    response = client.post(
        path=order_items_list_url,
        data={"scoops_requested": 2, "ice_cream_tub": ice_cream_tub.id},
    )
    assert response.status_code == 201
    response_data = json.loads(response.content)
    assert response_data == {
        "id": 1,
        "order": 1,
        "scoops_requested": 2,
        "ice_cream_tub": 1,
    }


def test_create_order_item_with_more_scoops_than_available_should_fail(
    client, order, ice_cream_tub
) -> None:
    response = client.post(
        path=order_items_list_url,
        data={"scoops_requested": 41, "ice_cream_tub": ice_cream_tub.id},
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "non_field_errors": [
            "Number of scoops_requested exceeds number of scoops available in ice cream tub."
        ]
    }
