from django.urls import path, include

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),

    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),


    path('addevent/', views.addevent, name='addevent'),
    path('events/', views.events, name='events'),   #contents list
    path('eventedit/<int:id>', views.eventedit, name='eventedit'),  #contentedit
    path('eventdelete/<int:id>', views.eventdelete, name='eventdelete'),
    path('eventaddimage/<int:id>', views.eventaddimage, name='eventaddimage'),

    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]