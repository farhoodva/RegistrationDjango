from django.urls import path, include
from .views import(

    RegistrationView,
    DriverInfoView,
    DriverInfoUpdate,
    load_cities,
    activate,
    DriverListView,
)

from .functions import render_pdf_view, export_excel

app_name = 'registration'


urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('', RegistrationView.as_view(), name='registration'),
    path('info_view', DriverInfoView.as_view(), name='info_view'),
    path('info_update/<pk>', DriverInfoUpdate.as_view(), name='info_update'),
    path('ajax/load_cities/', load_cities, name='load_cities'),
    path('activate/<token>', activate, name='activate'),
    path('list_view', DriverListView.as_view(), name='list_view'),
    path('list_view_pdf', render_pdf_view, name='list_view_pdf'),
    path('export_excel', export_excel, name='export_excel'),

]
