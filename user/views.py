from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from event.models import Category
from home.models import Setting, UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm
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


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'category': category,
                       'user_form': user_form,
                       'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') #Check login
def addtoactivity (request):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        form=AddActivityForm(request.POST)
        if form.is_valid():
            current_user=request.user
            data=AddActivity()
            data.user_id=current_user.id
            data.title = form.cleaned_data['title']
            data.name=form.cleaned_data['name']
            data.surname = form.cleaned_data['surname']
            data.image = form.cleaned_data['image']
            data.status = form.cleaned_data['status']
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
    return render(request, 'user_activity.html', context)


def change_password(request):
    if request.method=='POST':
        form =PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('/user')
        else:
            messages.error(request,'Please correct the error<br>'+str(form.errors))
            return redirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',{
            'form':form,'category': category})

