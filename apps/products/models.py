from django.db import models
import uuid
from config.utils_variables import categoriestable, productstable

# Create your models here.
class Categories(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = categoriestable

    def __str__(self):
        return self.category_name
		
		
class Products(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, default=None, db_column = 'category_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, default=None)
    product_image = models.CharField(max_length=255, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = productstable

    def __str__(self):
        return self.product_name

