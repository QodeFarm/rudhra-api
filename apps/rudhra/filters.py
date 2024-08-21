from django_filters import rest_framework as filters, CharFilter
from .models import Categories,Products
from config.utils_methods import filter_uuid


class CategoriesFilter(filters.FilterSet):
    category_id = filters.CharFilter(method=filter_uuid)
    category_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Categories
        fields =[]


class ProductsFilter(filters.FilterSet):
    product_id = filters.CharFilter(method=filter_uuid)
    product_name = filters.CharFilter(lookup_expr='icontains')
    category_id = filters.CharFilter(method=filter_uuid)
    category_name = CharFilter(field_name='category_id__category_name', lookup_expr='exact')
    price = filters.NumberFilter()

    class Meta:
        model = Products
        fields =[]

