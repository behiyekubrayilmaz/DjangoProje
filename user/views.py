from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from content.models import Menu, Content, ContentForm
from event.models import Category, Comment
from home.models import Setting, UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm
from user.models import AddActivityForm, AddActivity


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    #return HttpResponse(profile)
    context = {'category': category,
               'menu': menu,
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
        menu = Menu.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'category': category,
                   'menu': menu,
                   'user_form': user_form,
                   'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

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
        menu = Menu.objects.all()
        return render(request, 'change_password.html',{
            'form':form,'category': category,'menu': menu})

@login_required(login_url='/login') #Check login
def comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    comments= Comment.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'setting': setting,
               'menu': menu,
               'comments': comments,
               }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') #Check login
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.error(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')




@login_required(login_url='/login')  # Check login
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST,request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status= 'False'
            data.save()
            messages.success(request, 'Etkiliğiniz eklendi. Teşekkür ederiz.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Etkinliğiniz eklenemedi. Lütfen kontrol edip tekrar deneyiniz.' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        category = Category.objects.all()
        form = ContentForm()
        context = {'menu': menu,
                   'category': category,
                   'setting': setting,
                   'form': form, }
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')  # Check login
def contents(request):          #content list
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)  # eklenen etkinliklerin gösterilmesi
    context = {'menu': menu,
               'category': category,
               'setting': setting,
               'contents': contents, }
    return render(request, 'user_contents.html', context)


def contentdelete(request):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.error(request, 'Activity deleted..')
    return HttpResponseRedirect('/user/contents')


def contentedit(request,id):
    content =Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST,request.FILES,instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etkiliğiniz eklendi. Teşekkür ederiz.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Etkinliğiniz eklenemedi. Lütfen kontrol edip tekrar deneyiniz.' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/'+str(id))
    else:
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        category = Category.objects.all()
        form = ContentForm(instance=content)
        context = {'menu': menu,
                   'category': category,
                   'setting': setting,
                   'form': form, }
        return render(request, 'user_addcontent.html', context)