from django.shortcuts import render,HttpResponse,HttpResponseRedirect, get_object_or_404
from cntrydetails.models import Country
# Create your views here.
def Homepage(request):
    countries=Country.objects.all()
    return render(request,'base.html',context={"countries":countries})