from django.urls import path, include

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('activity/', views.activity, name='activity'),
    path('addtoactivity/', views.addtoactivity, name='addtoactivity'),

    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]