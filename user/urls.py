from django.urls import path, include

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('addtoactivity/<int:id>', views.addtoactivity, name='addtoactivity'),   #üyenin eklediği activity formdan gelen buton
    path('activity/', views.activity, name='activity'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),


    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]