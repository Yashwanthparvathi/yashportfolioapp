from django.urls import path
from . import views


urlpatterns = [
    path('', views.projectsda,name="projectsda"),  
    path('projects/<str:pk>/', views.projects,name="projects"),
    path('create-project/', views.createproject,name="create-project"),
    path('update-project/<str:pk>/', views.updateproject,name='update-project'),
    path('delete-project/<str:pk>/', views.deleteproject,name='delete-project'),
   
]
