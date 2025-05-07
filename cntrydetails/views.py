from .models import Country
from .serializers import CountryListSerializer,CountryDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import CreateUpdateCountrySerializer
# Create your views here.

#list of all Country
class CountryList(APIView):
    def get(self,request,*args,**kwargs):
        countrylist=Country.objects.all()
        serializer=CountryListSerializer(instance=countrylist,many=True)
        return Response(serializer.data)

class CountryDetails(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailsSerializer

    def get_object(self):
        common_name = self.kwargs.get('common_name')
        return get_object_or_404(Country, common_name__iexact=common_name)
    
#use this for browsable form in the browser
class CreateCountry(generics.CreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CreateUpdateCountrySerializer

#update and existing country details
class UpdateCountryDetails(generics.RetrieveUpdateAPIView):
    queryset=Country.objects.all()
    serializer_class=CreateUpdateCountrySerializer
    lookup_field = 'common_name'
    #for accessing name with anytype letter
    def get_object(self):
        common_name = self.kwargs.get('common_name')
        return get_object_or_404(Country, common_name__iexact=common_name)