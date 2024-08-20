from rest_framework import serializers
from apps.rudhra.models import Categories,Products


class ModCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_name']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
		
		
class ModProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_name','price']

class ProductsSerializer(serializers.ModelSerializer):
    category = ModCategoriesSerializer(source='category_id', read_only=True)
    class Meta:
        model = Products
        fields = '__all__'