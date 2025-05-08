from django.urls import path
from .views import Homepage

app_name='cntryinfo'
urlpatterns=[
  path('',Homepage,name='homepage'),
]