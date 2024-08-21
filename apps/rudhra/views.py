from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.rudhra.filters import CategoriesFilter, ProductsFilter
from config.utils_methods import list_all_objects,create_instance,update_instance
from apps.rudhra.serializers import CategoriesSerializer, ProductsSerializer 
from apps.rudhra.models import Categories,Products
from django.core.mail import send_mail
import json
from config.settings import EMAIL_HOST_USER
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Create your views here.
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CategoriesFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
		
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = ProductsFilter
    ordering_fields = []

    def list(self, request, *args, **kwargs):
        return list_all_objects(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return create_instance(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return update_instance(self, request, *args, **kwargs)
    

class SendmailViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            # Load JSON data from the request body
            data = request.data  # Use request.data instead of request.body

            # Extract data from the request
            categories = data.get('data', [])
            total_amount = data.get('total_amount', 0.00)

            # Prepare email content
            email_subject = 'Order Summary'
            email_body = f"Order Summary:\n\nTotal Amount: ${total_amount}\n\n"

            for category in categories:
                category_name = category.get('category_name')
                email_body += f"Category: {category_name}\n"
                
                for product in category.get('products', []):
                    product_name = product.get('product_name')
                    price = product.get('price')
                    quantity = product.get('quantity')
                    email_body += f"  Product: {product_name}, Price: ${price}, Quantity: {quantity}\n"
                
                email_body += "\n"

            # Sending email
            send_mail(
                subject=email_subject,
                message=email_body,
                # from_email='qodefarm7@gmail.com',  
                # recipient_list=['sruthi.konda@qodefarm.com'], 
                from_email=EMAIL_HOST_USER, 
                recipient_list=[data.get("data")[0].get('email')],  
                fail_silently=False,
            )
            return Response({'status': 'success', 'message': 'Email sent successfully.'})

        except json.JSONDecodeError:
            return Response({'status': 'error', 'message': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 