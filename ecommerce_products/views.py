from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db import transaction

from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ImportProductSerializer,
    MerchantSerializer,
)
from .models import Product, Merchant
from .services.product_import_service import import_product_from_external

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20

class MerchantCreateView(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet responsible for all product operations:
    - Import from external sources (Shopify, etc.)
    - Listing & filtering
    - Detail view
    - Bulk activation/deactivation
    - Soft deletion
    """
    queryset = Product.objects.all().prefetch_related("variants")
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer
        elif self.action == "import_external":
            return ImportProductSerializer
        return ProductDetailSerializer


    def get_queryset(self):
        """
        Filters queryset by merchant_id, active status, and search keyword.
        Supports case-insensitive search by product title.
        """
        queryset = self.queryset
        merchant_id = self.request.query_params.get("merchant_id")
        status_filter = self.request.query_params.get("active")
        search = self.request.query_params.get("search")

        if merchant_id:
            queryset = queryset.filter(merchant_id=merchant_id)
        if status_filter in ["true", "false"]:
            queryset = queryset.filter(active=(status_filter == "true"))
        if search:
            queryset = queryset.filter(Q(title__icontains=search))

        return queryset


    @action(detail=False, methods=["post"], url_path="import")
    def import_external(self, request):
        """
        Import product data from an external platform (e.g., Shopify).

        Example:
        POST /api/products/import/
        {
            "store_url": "merchant-store.myshopify.com",
            "product": {
                "id": "12345",
                "title": "Product Title",
                "description": "Product description",
                "product_type": "Electronics",
                "variants": [
                    {
                        "id": "67890",
                        "title": "Variant Name",
                        "sku": "SKU-001",
                        "price": "29.99",
                        "compare_at_price": "39.99",
                        "inventory_quantity": 100
                    }
                ]
            }
        }
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
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    @action(detail=False, methods=["post"], url_path="bulk-activate")
    def bulk_activate(self, request):
        """
        Bulk activate/deactivate multiple products.

        Example:
        POST /api/products/bulk-activate/
        {
            "product_ids": [1, 2, 3],
            "active": true
        }
        """
        product_ids = request.data.get("product_ids")
        active = request.data.get("active")

        if not isinstance(product_ids, list) or active is None:
            return Response(
                {"error": "Both 'product_ids' (list) and 'active' (bool) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            updated_count = Product.objects.filter(id__in=product_ids).update(active=active)

        return Response(
            {"updated_count": updated_count, "active_status": active},
            status=status.HTTP_200_OK,
        )


    @action(detail=True, methods=["post"], url_path="remove")
    def remove_product(self, request, pk=None):
        """
        Soft delete: marks product as inactive instead of deleting.

        Example:
        POST /api/products/{id}/remove/
        """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not product.active:
            return Response(
                {"message": "Product is already inactive."},
                status=status.HTTP_200_OK,
            )

        product.active = False
        product.save(update_fields=["active"])

        return Response(
            {"message": f"Product {product.id} deactivated successfully."},
            status=status.HTTP_200_OK,
        )
