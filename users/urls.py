from django.urls import path
from . import views


urlpatterns= [
    path('login/', views.loginuser, name = "login"),
    path('logout/', views.logoutuser, name = "logout"),
    path('register/', views.registeruser, name = "register"),
    path('',views.profiles,name="profiles"),
    path('profile/<uuid:pk>/profile.html',views.userprofile,name="user-profile"),
    path('account/', views.usersaccount, name="account"),
    path('edit-account/', views.editaccount, name="edit-account"),
    path('create-skill/', views.createskill, name="create-skill"),
    path('update-skill/<uuid:pk>/', views.updateskill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.deleteskill, name="delete-skill"),
    path('inbox/',views.inbox,name="inbox"),
    path('message/<str:pk>/',views.viewMessage,name="message"),
    path('create-message/<str:pk>/', views.createMessage, name="create-message")
    

]
