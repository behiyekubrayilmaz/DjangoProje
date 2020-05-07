from django.urls import path, include

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('addtoactivity/', views.addtoactivity, name='addtoactivity'),   #üyenin eklediği activity formdan gelen buton
    path('activity/', views.activity, name='activity'),
    path('password/', views.change_password, name='change_password'),

    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]