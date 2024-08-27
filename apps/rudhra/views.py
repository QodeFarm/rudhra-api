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
            data = request.data  # Use request.data instead of request.body

            # Extract data from the request
            categories = data.get('data', [])
            # provided_total_amount = data.get('total_amount', None)

            # # Compute total amount if not provided
            # computed_total_amount = 0.00
            # for category in categories[1:]:  # Start from the second item to skip the email item
            #     for product in category.get('products', []):
            #         price = product.get('price')
            #         quantity = product.get('quantity')
            #         computed_total_amount += price * quantity

            # total_amount = provided_total_amount if provided_total_amount is not None else computed_total_amount

            # Prepare email content
            email_subject = 'Order Summary'
            email_body = f"""
            <html>
            <body>
                <h2>Order Summary</h2>
                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th>SI.NO</th>
                            <th>Category</th>
                            <th>Product</th>
                            <th>Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            row_number = 1
            for category in categories[1:]:  # Start from the second item to skip the email item
                category_name = category.get('category_name')
                for product in category.get('products', []):
                    product_name = product.get('product_name')
                    # price = product.get('price')
                    quantity = product.get('quantity')
                    # total = price * quantity
                    email_body += f"""
                        <tr>
                            <td>{row_number}</td>
                            <td>{category_name}</td>
                            <td>{product_name}</td>
                            <td>{quantity}</td>
                        </tr>
                    """
                    row_number += 1

            # Add a final row for the total amount
            email_body += f"""
                    </tbody>
                </table>
            </body>
            </html>
            """

            # Extract and split emails
            email_str = categories[0].get('email')
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
