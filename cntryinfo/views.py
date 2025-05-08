from django.shortcuts import render,HttpResponse,HttpResponseRedirect, get_object_or_404
from cntrydetails.models import Country,CountryLanguage


# Create your views here.

def Homepage(request):
    countries=Country.objects.all()
    return render(request,'base.html',context={"countries":countries})


def SearchResult(request):
    query=request.GET.get('q','')
    if query:
        countries=Country.objects.filter(common_name__icontains=query)
        return render(request,'search.html',context={"countries":countries,'query':query})
    return render(request,'search.html',context={"countries":countries,'query':''})


def CountryDetails(request, pk):
    country = get_object_or_404(Country, pk=pk)
    # Get spoken languages
    languages = CountryLanguage.objects.filter(country=country).values_list('language__name', flat=True)
    # Get other countries in the same region (exclude itself)
    same_regional_countries = Country.objects.filter(region=country.region).exclude(pk=pk).values_list('common_name', flat=True)
    return render(request, 'country_details.html', context={
        'country': country,  
        'countries': list(same_regional_countries),
        'languages': list(languages),
    })