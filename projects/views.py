from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchprojects, paginateprojects

# projectslist = [
#     {
#        "id":"1",
#        "title":"ecommerce website",
#        "description":"fully functional ecommerce app", 
        
#     },
#         {
#        "id":"2",
#        "title":"portfolio website",
#        "description":"fully functional portfolio app", 
        
#     },
#       {
#        "id":"3",
#        "title":"social network",
#        "description":"fully functional social network app", 
        
#     },   
    
# ]

def projectsda(request):
    projects, search_query = searchprojects(request)
    custom_range ,projects = paginateprojects(request, projects, 2)
    

    context={"projects":projects,'search_query': search_query,'custom_range': custom_range}
    return render(request,"projects/projects.html",context)
    
def projects(request,pk):
  projectobj = Project.objects.get(id=pk)
  form  = ReviewForm()
  tags = projectobj.tags.all()
  # print('projectobj:', projectobj)
  if request.method == 'POST':
      form = ReviewForm(request.POST)
      review = form.save(commit=False)
      review.project = projectobj
      review.owner = request.user.profile
      review.save()
      projectobj.getvotecount           
      #update project votecount
      messages.success(request,'your review was successfully submitted')
      return redirect('projects', pk=projectobj.id)
             
  return render(request,"projects/single-project.html",{"project":projectobj,"tags":tags,'form':form})

@login_required(login_url="login")
def createproject(request):
  profile = request.user.profile
  form = ProjectForm()
  
  if request.method == "POST":
      # print(request.POST)
      form = ProjectForm(request.POST, request.FILES)
      if form.is_valid():
        project = form.save(commit = False)
        project.owner = profile
        project.save()
      # return redirect('projects',pk=projects.pk)
      return redirect('account')
    
  context = {"form":form}
  return render(request, "projects/project_form.html",context)


@login_required(login_url="login")
def updateproject(request,pk):
  profile = request.user.profile
  # project = Project.project_set.objects.get(id=pk)
  projectss = profile.project_set.get(id=pk)
  form = ProjectForm(instance=projectss)
  
  if request.method == "POST":
    
     form = ProjectForm(request.POST,request.FILES,instance=projectss)
     if form.is_valid():
         form.save()
     return redirect("account")
    
  context = {"form":form}
  return render(request, "projects/project_form.html",context)

@login_required(login_url="login")
def deleteproject(request,pk):
  profile = request.user.profile
  # delproject = Project.objects.get(id=pk)
  delproject = profile.project_set.get(id=pk)
  if request.method == 'POST':
    delproject.delete()
    return redirect('account')
  context= {'object':delproject}
  return render(request, "delete_template.html",context)