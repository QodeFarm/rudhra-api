from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.rudhra.filters import CategoriesFilter, ProductsFilter
from config.utils_methods import list_all_objects,create_instance,update_instance
from apps.rudhra.serializers import CategoriesSerializer, ProductsSerializer 
from apps.rudhra.models import Categories,Products
import json
from config.settings import EMAIL_HOST_USER
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

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
            data = request.data

            # Extract email and categories from the request
            email_str = data.get('email')
            categories = data.get('data', [])

            # Prepare email content
            email_subject = 'Order Summary'
            email_body = f"""
            <html>
            <body>
                <h2>Order Summary</h2>
                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th>S.No</th>
                            <th>Category</th>
                            <th>Product</th>
                            <th>Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            row_number = 1
            for category in categories:
                category_name = category.get('category_name')
                for product in category.get('products', []):
                    product_name = product.get('product_name')
                    quantity = product.get('quantity')
                    email_body += f"""
                        <tr>
                            <td>{row_number}</td>
                            <td>{category_name}</td>
                            <td>{product_name}</td>
                            <td>{quantity}</td>
                        </tr>
                    """
                    row_number += 1

            email_body += f"""
                    </tbody>
                </table>
            </body>
            </html>
            """

            # Split emails into a list
            recipient_list = [email.strip() for email in email_str.split(',')]

            # Sending email
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=EMAIL_HOST_USER,  # Ensure you have your email host user configured
                to=recipient_list,
            )
            email.content_subtype = "html"  # Set the email content type to HTML
            email.send(fail_silently=False)

            return Response({'status': 'success', 'message': 'Email sent successfully.'})

        except json.JSONDecodeError:
            return Response({'status': 'error', 'message': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
