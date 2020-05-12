from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import CommenttForm, Commentt


def index(request):
    return HttpResponse("Content Page")


@login_required(login_url='/login') #Check login
def addcomment (request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        form=CommenttForm(request.POST)
        if form.is_valid():
            current_user=request.user
            data=Commentt()
            data.user_id=current_user.id
            data.content_id=id
            data.subject=form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Yorumunuz basarılı bir şekilde gönderildi. Teşekkür ederiz.")
            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol edip tekrar deneyiniz.")
    return HttpResponseRedirect(url)