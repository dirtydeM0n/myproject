from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.apps import apps
from django.db import connection
from django.shortcuts import get_object_or_404

from myproject.models import BioData, ItemData, Stock, UserLogin

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate



@method_decorator(csrf_exempt, name='dispatch')
class TableDataAPI(View):
    def get(self, request, *args, **kwargs):
        table_name = request.GET.get('report_name')

        # Get the model based on the table name
        model = {}
        try:
                model = apps.get_model(app_label='myproject', model_name=table_name)
        except LookupError:
                pass 

        if model:
            # Retrieve data from the model
            data = list(model.objects.values())
            response_data = {'data': data}
            return JsonResponse(response_data)

        response_data = {'error': 'Table not found'}
        return JsonResponse(response_data, status=404)
    

@method_decorator(csrf_exempt, name='dispatch')
class ExistingTablesAPI(View):

    EXCLUDE_TABLES = [
        "auth_group",
        "auth_group_permissions",
        "auth_permission",
        "auth_user",
        "auth_user_groups",
        "auth_user_user_permissions",
        "django_admin_log",
        "django_content_type",
        "django_migrations",
        "django_session",
    ]

    def get(self, request, *args, **kwargs):
        # Get the table names from the database
        table_names = connection.introspection.table_names()

        # Exclude specified table names
        filtered_table_names = [name.split('myproject_')[1] for name in table_names if name not in self.EXCLUDE_TABLES and name.startswith('myproject_')]

        response_data = {'reports': filtered_table_names}
        return JsonResponse(response_data)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class BioDataCreateAPI(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the request data as JSON
            request_data = json.loads(request.body.decode('utf-8'))

            # Extract data from the request
            name = request_data.get('name')
            address = request_data.get('address')
            location = request_data.get('location')

            # Create a new BioData instance and save it to the database
            biodata = BioData.objects.create(name=name, address=address, location=location)

            response_data = {'message': 'Data inserted successfully'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class ItemDataCreateAPI(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the request data as JSON
            request_data = json.loads(request.body.decode('utf-8'))

            # Extract data from the request
            name = request_data.get('name')
            description = request_data.get('description')
            category = request_data.get('category')

            # Create a new BioData instance and save it to the database
            itemdata = ItemData.objects.create(name=name, description=description, category=category)

            response_data = {'message': 'Data inserted successfully'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

def create_item_data_instance(item_id):
    # Retrieve the data associated with the item_id
    item_data = get_object_or_404(ItemData, id=item_id)

    # Create a new ItemData instance
    new_item_data_instance = ItemData(
        id=item_id,
        name=item_data.name,
        description=item_data.description,
        category=item_data.category,
        price=item_data.price
    )

    # Save the new ItemData instance
    new_item_data_instance.save()

    return new_item_data_instance

@method_decorator(csrf_exempt, name='dispatch')
class StockAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the request data as JSON
            request_data = json.loads(request.body.decode('utf-8'))

            # Extract data from the request
            item = create_item_data_instance(request_data.get('item_id'))
            qty = request_data.get('qty')
            basic_price = request_data.get('basic_price')
            selling_price = request_data.get('selling_price')

            # Create a new BioData instance and save it to the database
            itemdata = Stock.objects.create(item=item, qty=qty, basic_price=basic_price, selling_price=selling_price)

            response_data = {'message': 'Data inserted successfully'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
@api_view(['POST'])
@permission_classes([AllowAny])
def UserLoginAPI(request):

        username = request.data.get("username")
        password =  request.data.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
# Create a new user using create_user method.
@api_view(['POST'])
def UserCreate(request):

    username = request.data.get("username")
    password =  request.data.get("password")
    email =  request.data.get("email")

    
    # Create a new user using the custom manager
    user = UserLogin.objects.create_user(username, email, password)

        # Optionally, set other user fields
    user.is_active = True
    user.save()

    return Response({"message": "Register successful"}, status=status.HTTP_200_OK)