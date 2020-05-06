from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from event.models import Category
from home.models import Setting, UserProfile
from user.models import AddActivityForm, AddActivity


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(pk=current_user.id)
    #return HttpResponse(profile)
    context = {'category': category,
               'setting': setting,
               'profile': profile,
               }
    return render(request, "user_profile.html",context)

@login_required(login_url='/login') #Check login
def addtoactivity (request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        form=AddActivityForm(request.POST)
        if form.is_valid():
            current_user=request.user
            data=AddActivity()
            data.user_id=current_user.id
            data.name=form.cleaned_data['name']
            data.surname = form.cleaned_data['surname']
            data.title = form.cleaned_data['title']
            data.detail = form.cleaned_data['detail']
            data.save()
            messages.success(request,"Yorumunuz basarılı bir şekilde gönderildi. Teşekkür ederiz.")
            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol edip tekrar deneyiniz.")
    return HttpResponseRedirect(url)


def activity(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    # return HttpResponse(profile)
    context = {'category': category,
               'setting': setting,
               }
    return render(request, "user_activity.html", context)