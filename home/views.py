from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from event.models import Event, Category, Images
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata =Event.objects.all()[:4]
    category=Category.objects.all()
    dayevents=Event.objects.all()[:4]
    lastyevents = Event.objects.all().order_by('-id')[:4]
    randomevents= Event.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'dayevents': dayevents,
               'lastyevents': lastyevents,
               'randomevents': randomevents,
               'category':category,
               'page':'home',
               'sliderdata':sliderdata}
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'catego ry': category,
               'page':'aboutus'}
    return render(request, 'aboutus.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'page':'references'}
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

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form=ContactFormu()
    context = {'setting': setting,
               'category': category,
               'form':form}
    return render(request, 'contact.html', context)


def category_events(request,id,slug):
    events = Event.objects.filter(category_id=id)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    context = {'events': events,
               'category': category,
               'categorydata':categorydata}
    return render(request, 'events.html', context)

def event_detail(request,id,slug):
    events = Event.objects.get(pk=id)
    category = Category.objects.all()
    images =Images.objects.filter(event_id=id)
    context = {'events': events,
               'category': category,
               'images': images,}
    return render(request, 'event_detail.html', context)
