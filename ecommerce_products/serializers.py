from rest_framework import serializers
from .models import Product, Variant, Merchant

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["id", "name", "email", "store_url", "status", "created_at"]
        read_only_fields = ["id", "created_at"]


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            "external_id",
            "name",
            "sku",
            "price",
            "retail_price",
            "quantity",
            "active",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'base_price', 'active', 'image_url']

    def get_image_url(self, obj):
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "external_id",
            "title",
            "description",
            "product_type",
            "active",
            "base_price",
            "created_at",
            "variants",
        ]


class ImportVariantSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    sku = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    inventory_quantity = serializers.IntegerField()


class ImportProductSerializer(serializers.Serializer):
    store_url = serializers.CharField()
    product = serializers.DictField()

    def validate(self, data):
        product_data = data.get("product", {})
        required_fields = ["id", "title", "variants"]

        for field in required_fields:
            if field not in product_data:
                raise serializers.ValidationError(f"Missing required field '{field}' in product data.")

        if not isinstance(product_data["variants"], list):
            raise serializers.ValidationError("Variants must be a list.")

        return data
