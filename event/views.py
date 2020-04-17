from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from event.models import CommentForm, Comment


def index(request):
    return HttpResponse("Event Page")

@login_required(login_url='/login') #Check login
def addcomment (request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user
            data=Comment()
            data.user_id=current_user.id
            data.event_id=id
            data.subject=form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Yorumunuz basarılı bir şekilde gönderildi. Teşekkür ederiz.")
            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol edip tekrar deneyiniz.")
    return HttpResponseRedirect(url)