from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm , MessageForm
from .utils import searchprofiles,paginateprofiles

# Create your views here.

def loginuser(request):
    page = 'register'
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == "POST":
        # print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        # except User.DoesNotExist:
        except:
            # print("Username does not exist")  
            # print("Username does not exist") 
            messages.error(request,'username doesnot exist')
        
        user = authenticate(request, username = username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
           messages.error(request,"username or password is incorrect")  
    return render(request, "users/login_register.html")


def logoutuser(request):
    logout(request)
    messages.info(request,'user was logged out')
    return redirect('login')

def registeruser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User account was created')
            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.success(request, "An error has occurred during registration")
            
    context = {'page':page,'form':form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchprofiles(request)
    
    custom_range, profiles = paginateprofiles(request,profiles,3)
        
    context = {'profiles':profiles,'search_query': search_query,'custom_range':custom_range}
    return render(request, 'users/profiles.html',context)

# def userprofile(request,pk):
#  profile = Profile.objects.get(id=pk)
#  topskills = profile.skill_set.exclude(description__exact = "")
#  otherskills = profile.skill_set.filter(description="")
#  context = {'profile':profile,"topskills":topskills,"otherskills":otherskills}
#  return render(request,'users/user-profile.html',context)
def userprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skills.exclude(description__exact="")
    otherskills = profile.skills.filter(description="")
    context = {'profile': profile, "topskills": topskills, "otherskills": otherskills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def usersaccount(request):
    profile = request.user.profile
    skills = profile.skills.all()
    projects = profile.project_set.all()
      
    context = {'profile':profile,'topskills':skills,'projects':projects }
    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editaccount(request):
    profile=request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == "POST":
        form=ProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save( )
            return redirect('account')
    context = {'form': form }
    return render(request,'users/profile_form.html', context)

@login_required(login_url='login')
def createskill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "skill was added successfully")
            return redirect('account')
    
    context = { 'form':form }
    return render(request, 'users/skill_form.html',context)



@login_required(login_url='login')
def updateskill(request,pk):
    profile = request.user.profile
    skill = profile.skills.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            # skill = form.save(commit=False)
            # skill.owner = profile
            form.save()
            messages.success(request, "skill was updated successfully")
            return redirect('account')
    
    context = { 'form':form }
    return render(request, 'users/skill_form.html',context)


def deleteskill(request,pk):
    profile = request.user.profile
    skill = profile.skills.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "skill was deleted successfully")
        return redirect('account')
    context = {'object':skill}
    return render(request,'delete_template.html',context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadcount =  messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests, 'unreadCount':unreadcount}
    return render(request,"users/inbox.html",context)


@login_required(login_url='login')

def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        
      message.is_read = True
      message.save()
    context = {'message':message}
    return render(request, 'users/message.html',context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    try:
        sender = request.user.profile 
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
                message.save()
            
            messages.success(request,'your message was successfully sent')
            return redirect('user-profile', pk=recipient.id)
    context = {'recipient':recipient,'form':form }
    return render(request, 'users/message_form.html', context)