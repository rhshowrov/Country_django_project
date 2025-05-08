from django.urls import path
from .views import Homepage,SearchResult

app_name='cntryinfo'
urlpatterns=[
  path('',Homepage,name='homepage'),
  path('search/',SearchResult,name='search'),
]