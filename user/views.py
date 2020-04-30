from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from event.models import Category
from home.models import Setting, UserProfile


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