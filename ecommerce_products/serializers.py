from rest_framework import serializers
from .models import Product, Variant

# --- Basic serializers ---

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['external_id', 'name', 'sku', 'price', 'retail_price', 'quantity', 'active']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'product_type', 'base_price', 'active']


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'external_id', 'title', 'description', 'product_type',
            'base_price', 'active', 'variants'
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
