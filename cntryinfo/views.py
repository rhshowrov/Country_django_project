from django.shortcuts import render,get_object_or_404, redirect
from cntrydetails.models import Country,CountryLanguage
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cntryinfo:homepage')  
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {
        'form': form,
        'title': 'Register'
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cntryinfo:homepage')  
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'title': 'Login'
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def Homepage(request):
    countries=Country.objects.all()
    return render(request,'base.html',context={"countries":countries})

@login_required
def SearchResult(request):
    query=request.GET.get('q','')
    if query:
        countries=Country.objects.filter(common_name__icontains=query)
        return render(request,'search.html',context={"countries":countries,'query':query})
    return render(request,'search.html',context={"countries":countries,'query':''})

@login_required
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