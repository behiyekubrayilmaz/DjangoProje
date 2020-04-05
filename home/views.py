from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from event.models import Event
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata =Event.objects.all()[:4]
    context = {'setting': setting,
               'page':'home',
               'sliderdata':sliderdata}
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'aboutus'}
    return render(request, 'aboutus.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'references'}
    return render(request, 'references.html', context)

def contact(request):

    if request.method=='POST':
        form=ContactFormu(request.POST)
        if form.is_valid():
            data =ContactFormMessage()
            data.name =form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()  #veritabanına kaydet
            messages.success(request,"Mesajınız başarı ile gönderildi")
            return HttpResponseRedirect ('/contact')

    setting = Setting.objects.get(pk=1)
    form=ContactFormu()
    context = {'setting': setting, 'form':form}
    return render(request, 'contact.html', context)

