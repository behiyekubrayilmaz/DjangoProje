from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Content, Menu, CImages
from event.models import Event, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata =Event.objects.all()[:4]
    category=Category.objects.all()
    menu = Menu.objects.all()
    dayevents=Event.objects.all()[:4]
    news = Content.objects.filter(type='haber').order_by('-id')[:4]
    announcements= Content.objects.filter(type='duyuru').order_by('-id')[:3]

    context = {'setting': setting,
               'dayevents': dayevents,
               'news': news,
               'announcements': announcements,
               'menu':menu,
               'category': category,
               'page':'home',
               'sliderdata':sliderdata}
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
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
    setting = Setting.objects.get(pk=1)
    comments=Comment.objects.filter(event_id=id,status='True')
    images =Images.objects.filter(event_id=id)
    context = {'events': events,
               'setting': setting,
               'category': category,
               'comments': comments,
               'images': images,}
    return render(request, 'event_detail.html', context)


def event_search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            query =form.cleaned_data['query']
            category = Category.objects.all()
            events = Event.objects.filter(title__icontains=query)
            context = {'events': events,
                       'category': category, }
            return render(request, 'events_search.html', context)
    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Lütfen kontrol ediniz")
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'category': category,
               'setting': setting,}
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form =SignUpForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'category': category,
            'setting': setting,
            'form':form,}
    return render(request, 'signup.html', context)


def menu(request,id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, 'Hata!')
        link='/error'
        return HttpResponseRedirect(link)

def contentdetail(request,id,slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    setting = Setting.objects.get(pk=1)
    try:
        content = Content.objects.get(pk=id)
        images = CImages.objects.filter(content_id=id)
        context = {'content': content,
               'setting': setting,
               'category': category,
               'menu': menu,
               'images': images, }
        return render(request, 'content_detail.html', context)
    except:
        messages.warning(request, 'Hata!')
        link = '/error'
        return HttpResponseRedirect(link)

def error(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {'category': category,
               'setting': setting,
               'menu': menu, }
    return render(request, 'error_page.html', context)