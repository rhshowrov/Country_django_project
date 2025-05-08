from django.shortcuts import render,HttpResponse,HttpResponseRedirect, get_object_or_404
from cntrydetails.models import Country
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