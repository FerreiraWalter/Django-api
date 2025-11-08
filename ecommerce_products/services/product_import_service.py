from django.db import transaction, IntegrityError
from ecommerce_products.models import Merchant, Product, Variant

@transaction.atomic
def import_product_from_external(validated_data):
    store_url = validated_data["store_url"]
    product_data = validated_data["product"]

    try:
        merchant = Merchant.objects.get(store_url=store_url)
    except Merchant.DoesNotExist:
        raise ValueError("Merchant with the given store_url does not exist.")

    external_id = product_data["id"]

    try:
        product, created = Product.objects.get_or_create(
            merchant=merchant,
            external_id=external_id,
            defaults={
                "title": product_data.get("title", ""),
                "description": product_data.get("description", ""),
                "product_type": product_data.get("product_type", ""),
                "base_price": product_data["variants"][0]["price"]
                if product_data.get("variants") else 0.0,
            },
        )
    except IntegrityError:
        raise ValueError("A product with this external_id already exists for this merchant.")

    if not created:
        return product, False

    variants_to_create = []
    for v in product_data["variants"]:
        retail_price = v.get("compare_at_price") or v["price"]
        variants_to_create.append(
            Variant(
                product=product,
                external_id=v["id"],
                name=v["title"],
                sku=v.get("sku", ""),
                price=v["price"],
                retail_price=retail_price,
                quantity=v.get("inventory_quantity", 0),
            )
        )

    Variant.objects.bulk_create(variants_to_create)

    return product, True
