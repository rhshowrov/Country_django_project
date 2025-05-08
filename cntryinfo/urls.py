from django.urls import path
from .views import Homepage,SearchResult,CountryDetails

app_name='cntryinfo'
urlpatterns=[
  path('',Homepage,name='homepage'),
  path('search/',SearchResult,name='search'),
  path('<str:pk>/details/', CountryDetails, name='country_details')

]