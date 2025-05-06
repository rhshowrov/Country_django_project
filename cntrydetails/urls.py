from django.urls import path
from .views import CountryList,CountryDetails
urlpatterns = [
    path('list/all/',CountryList.as_view(),name='country_list'),
    path('<str:common_name>/details/',CountryDetails.as_view(),name='country_list'),
]