from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ecommerce_products.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ImportProductSerializer
)
from ecommerce_products.models import Product
from ecommerce_products.services.product_import_service import import_product_from_external

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("merchant").prefetch_related("variants").all()
    serializer_class = ProductDetailSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["post"], url_path="import")
    def import_external(self, request):
        """
        Importa produto de fonte externa (Shopify, etc.)
        """
        serializer = ImportProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid request data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product, created = import_product_from_external(serializer.validated_data)
            msg = "Product imported successfully." if created else "Product already exists."
            return Response(
                {"id": product.id, "message": msg},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
