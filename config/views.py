from django.http import HttpResponse
from django.urls import reverse



def api_links(request):
    #Here we need to define the list of API endpoints and their names
    api_endpoints = [
        ('api/v1/products/', 'Products API'),
        ('swagger/','Swagger')
    ]

    html = """
    <html>
    <head>
        <style>
            body {
                background: linear-gradient(to right, #ece9e6, #ffffff); /* A subtle gradient background */
                font-family: 'Arial', sans-serif;
                color: #333;
                padding: 20px;
            }
            h1 {
                font-size: 24px;
                color: #4CAF50;
                margin-bottom: 20px;
            }

            li {
                margin: 10px 0;
            }
            a {
                text-decoration: none;
                color: #2196F3;
                font-weight: bold;
                font-size: 18px;
            }
            a:hover {
                color: #0D47A1;
            }
        </style>
    </head>
    <body>
        <h1>API Endpoints</h1>
        <ul>
    """

    for endpoint, name in api_endpoints:
        link = reverse('api_links') + endpoint
        html += f"<li><a href='{link}'>{name}</a></li>"

    return HttpResponse(html)
