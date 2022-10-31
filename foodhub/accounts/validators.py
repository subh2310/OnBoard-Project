from rest_framework import serializers
from accounts.models import Item
from silk.profiling.profiler import silk_profile
from functools import reduce
from operator import add
import structlog

log = structlog.get_logger()


@silk_profile(name='Validate_Store_Merchant')
def validate_store_merchant(data):
    """
    Checks if the Store's Merchant is same as Order's Merchant.
    """
    log.msg('Validating Store Merchant', data=data)
    store_merchant_id = data['store'].merchant.id
    order_merchant_id = data['merchant'].id
    if store_merchant_id != order_merchant_id:
        raise serializers.ValidationError(
            {"store": "Merchant ID doesn't match with Order's Merchant."})


@silk_profile(name='Validate_Items_Merchant')
def validate_items_merchant(data):
    """
    # Checks if the Items' Merchant is same as Model's Merchant.
    """
    log.msg('Validating Items Merchant', data=data)
    model_merchant_id = data['merchant'].id
    item_ids = [item.id for item in data['items']]
    item_merchant_ids = [item.merchant.id for item in Item.objects.filter(
        id__in=item_ids).select_related('merchant')]
    for item_merchant_id in item_merchant_ids:
        if item_merchant_id != model_merchant_id:
            raise serializers.ValidationError(
                {"items": "Item(s) do not belong to the selected Merchant."})


@silk_profile(name="Validate Total Cost")
def validate_total_cost(data):
    """
    Checks if the Total Cost is equal to the sum of Item Costs.
    """
    log.msg('Validating Total Costs', data=data)
    item_costs_list = [item.cost for item in data['items']]
    sum_item_costs = reduce(add, item_costs_list)
    if sum_item_costs != data["total_cost"]:
        raise serializers.ValidationError(
            {"total_cost": "Total Cost is Incorrect."})


"""
@silk_profile(name='Validate_Items_Merchant')
def validate_items_merchant(data):
    """
# Checks if the Items Merchant is same as Model's Merchant.
"""
    model_merchant_id = data['merchant'].id
    item_merchant_ids = [item.merchant.id for item in data['items']]
    for item_merchant_id in item_merchant_ids:
        if item_merchant_id != model_merchant_id:
            raise serializers.ValidationError(
                {"items": "Item(s) do not belong to the selected Merchant."})
"""
