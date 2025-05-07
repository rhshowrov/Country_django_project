from django.urls import path
from .views import CountryList,CountryDetails,CreateCountry, \
UpdateCountryDetails,DeleteCountry,SameRegionalCountry
urlpatterns = [
    path('list/all/',CountryList.as_view(),name='country_list'),
    path('<str:common_name>/details/',CountryDetails.as_view(),name='country_details'),
    path('create/',CreateCountry.as_view(),name='create_country'),
    path('<str:common_name>/update/',UpdateCountryDetails.as_view(),name='country_update'),
    path('delete/<str:common_name>/',DeleteCountry.as_view(),name='country_delete'),
    path('<str:common_name>/same_region_country/',SameRegionalCountry.as_view(),name='same_regional_country'),
]   