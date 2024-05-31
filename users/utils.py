from .models import Profile, Skills
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def paginateprofiles(request,profiles,results):
    page = request.GET.get('page')
   
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
      page = 1
      profiles = paginator.page(page)
    except EmptyPage:
      page = paginator.num_pages
      profiles = paginator.page(page)
      
      
    leftindex = (int(page) - 4)
    
    if leftindex < 1:
      leftindex = 1
      
    rightindex = (int(page) + 5)
    
    if rightindex > paginator.num_pages:
      # rightindex = paginator.num_pages + 1
      rightindex = paginator.num_pages + 1
    
    # custom_range = range(1, 20)
    custom_range = range(leftindex, rightindex)
    
    return custom_range,profiles


def searchprofiles(request):
    search_query =''
    skills = Skills.objects.none() 
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
        skills = Skills.objects.filter(name__icontains=search_query)

         # print('SEARCH:', search_query)   
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skills__in=skills)
        
        
        )
    
    return profiles, search_query