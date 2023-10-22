# myproject/myapp/urls.py

from django.urls import path
from django.views.generic import TemplateView

from .views import TableDataAPI, ExistingTablesAPI,BioDataCreateAPI, ItemDataCreateAPI, StockAPIView, UserLoginAPI, UserCreate

urlpatterns = [
    path('report-data/', TableDataAPI.as_view(), name='table_data_api'),
    path('all-reports/', ExistingTablesAPI.as_view(), name='existing_tables_api'),
    path('biodata/create/', BioDataCreateAPI.as_view(), name='biodata_create_api'),
    path('itemdata/create/', ItemDataCreateAPI.as_view(), name='itemdata_create_api'),
    path('stocks/create/', StockAPIView.as_view(), name='stock-api'),
    path('api/login/', UserLoginAPI, name='user_login'),
    path('api/register/', UserCreate, name='user_register'),
    path('home/', TemplateView.as_view(template_name='templates/index.html'), name='html_view'),

]
