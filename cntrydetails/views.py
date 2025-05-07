from .models import Country
from .serializers import CountryListSerializer,CountryDetailsSerializer,CountrySerializer
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
#retrive first to populate the form data for seamless update
class UpdateCountryDetails(generics.RetrieveUpdateAPIView):
    queryset=Country.objects.all()
    serializer_class=CreateUpdateCountrySerializer
    lookup_field = 'common_name'
    #for accessing name with anytype letter
    def get_object(self):
        common_name = self.kwargs.get('common_name')
        return get_object_or_404(Country, common_name__iexact=common_name)
    

#delete an existing country
#can be done using previous update details with some cahnges in url pattern
#usees of genericAPIVIEW
from rest_framework.generics import GenericAPIView
class DeleteCountry(GenericAPIView):
    queryset=Country.objects.all()
    serializer_class=CountrySerializer
    lookup_field='common_name'
    def get_object(self):
        return get_object_or_404(Country,common_name__iexact=self.kwargs.get(self.lookup_field))
    def delete(self, request, *args, **kwargs):
        country = self.get_object()
        country.delete()
        return Response({"success": "Deleted Successfully"}, status=status.HTTP_200_OK)

class SameRegionalCountry(generics.ListAPIView):
    lookup_field='common_name'

    def get_object(self):
        return get_object_or_404(Country,common_name__iexact=self.kwargs.get(self.lookup_field))
    
    def get_queryset(self):
        country=self.get_object()
        region=country.region
        subregion=country.subregion
        queryset=Country.objects.filter(region=region,subregion=subregion)
        return queryset
    
    #overriding list to modify response
    def list(self,request,*args,**kwargs):
        country=self.get_object()
        countries=self.get_queryset().values_list('common_name', flat=True)
        return Response({
            "region":country.region.name,
            "subregion":country.subregion.name,
            "countries":countries
        })    
