from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import ClimbingRoutes, Category, RouteGrade
from .forms import AddRouteForm, EditRouteForm
from members.forms import UserProfileForm
from members.models import UserProfile
from geopy.geocoders import Nominatim
from django.core.paginator import Paginator
import geopy.geocoders
import ssl
import certifi



def main_dashboard(request):
    latest_routes = ClimbingRoutes.objects.all().order_by('-added')[:5:1]
    ######################
    category_objects_quantity=[]
    categories=[]
    category_names = Category.objects.all()
    for catego in category_names:
        category_objects_quantity.append(ClimbingRoutes.objects.filter(category=catego).count())
    for category_name in category_names:
        categories.append(str(category_name))
    ######################
    ####### total sum of routes for 3 best ###########################
    routes_quantity={}
    for user in User.objects.all():
        sum=0
        routes_total = ClimbingRoutes.objects.filter(user=user)
        for route in routes_total:
                sum=sum+1
        routes_quantity[user.username]=sum
        routes_quantity_sorted=sorted(routes_quantity.items(),key=lambda x:x[1])[-1:-6:-1]
        routes_quantity_sorted=dict((x,y) for x,y in routes_quantity_sorted)
    best_climbers=[]
    best_results=[]
    for climber in routes_quantity_sorted.keys():
        best_climbers.append(climber)
    for best_value in routes_quantity_sorted.values():
        best_results.append(best_value)
    ##################################################################
    ############ Most popular climber ################################
    all_profiles = {}
    for climber in User.objects.all():
        total_likes=climber.userprofile.likes.count()
        all_profiles[climber]=total_likes
    best_profile=sorted(all_profiles.items(),key=lambda x:x[1])[-1]
    best_profile_user_name=best_profile[0]
    best_profile_likes_total=best_profile[1]
    ##################################################################
    ############ Best Routes in Categories ###########################
    best_users = {}
    for category in Category.objects.all():
        all_grades=[]
        category_grades=RouteGrade.objects.filter(category=category).order_by('order_number')[::-1]
        for route in category_grades:
            all_grades.append(route)
        for grade in all_grades:
            try:
                best=ClimbingRoutes.objects.filter(official_grade=grade.id)[0]
                best_users[category.category]=best
                break
            except Exception:
                continue

    ##################################################################
    ############# RETURNING LOCATIONS OF USERS TO SHOW ON MAP ########
    profiles=UserProfile.objects.all()
    locations=[]
    coordinates_list={}
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(user_agent='Rock and Climb',scheme='http')
    for profile in profiles:
        if profile.where_lives !='' and profile.where_lives != None:
            locations.append(profile.where_lives)
    try:
        for location in locations:
            coord=geolocator.geocode(location)
            coordinates=[coord.latitude, coord.longitude]
            coordinates_list[location]=coordinates
    except Exception:
        coordinates_list={}
    ##################################################################
    return render(request,'main_dashboard.html',{'latest_routes':latest_routes,'category_objects_quantity':category_objects_quantity,
                                                 'categories':categories,'routes_quantity_sorted':routes_quantity_sorted,
                                                 'best_climbers':best_climbers,'best_results':best_results,
                                                 'best_profile_user_name':best_profile_user_name,
                                                 'best_profile_likes_total':best_profile_likes_total,
                                                 'best_in_categories':best_users, 'coordinates_list':coordinates_list})

def all_routes(request,category):
    all_routes = ClimbingRoutes.objects.all().order_by('-added')
    categories = Category.objects.all()
    if category == 'all':
        paginator = Paginator(all_routes,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'all_routes.html',{'all_routes':page_obj, 'categories':categories,'actual_category':category})
    all_routes = ClimbingRoutes.objects.filter(category=category).order_by('-added')
    paginator = Paginator(all_routes,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'all_routes.html',{'all_routes':page_obj,'categories':categories,'actual_category':category})

@login_required
def load_grades(request):
    category = request.GET.get('category')
    category=Category.objects.get(category=category)
    grades = RouteGrade.objects.filter(category=category).order_by('order_number')
    return render(request,'grades_drop_down.html',{'grades':grades})

@login_required
def add_route(request):
    if request.method == 'POST':
        form = AddRouteForm(request.POST)
        if form.is_valid():
            form2=form.save(commit=False)
            form2.user=request.user
            form2.save()
            messages.success(request,'Your climbing was added to the database...')
            return HttpResponseRedirect(reverse('add_route'))
        else:
            messages.warning(request,'Cannot save Your climbing, please check errors below...')

    else:
        form = AddRouteForm()
    return render(request,'add_route.html',{'form':form})

@login_required
def my_profile(request,category):
    all_routes = ClimbingRoutes.objects.filter(user=request.user).order_by('-added')
    user_info = get_object_or_404(User,pk=request.user.id)
    ########### IS USER BEGINEER, SEMI, ADVANCED, PRO ########################
    total_routes = all_routes.count()
    user_level = user_level_counting(total_routes)
    ##########################################################################
    ########### STATISTICS ###################################################
    category_objects_quantity = []
    categories_list = []
    category_names = Category.objects.all()
    for catego in category_names:
        category_objects_quantity.append(ClimbingRoutes.objects.filter(category=catego, user=user_info).count())
    for category_name in category_names:
        categories_list.append(str(category_name))
    if (category_objects_quantity == [0,0,0,0,0]):
        category_objects_quantity = []
    ##########################################################################
    categories = Category.objects.all()
    if category == 'all':
        paginator = Paginator(all_routes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'my_profile.html',{'all_routes':page_obj, 'categories':categories,
                                                 'actual_category':category,'user_info':user_info,
                                                 'user_level':user_level, 'category_objects_quantity':category_objects_quantity,
                                                 'categories_list':categories_list})
    all_routes = ClimbingRoutes.objects.filter(user=request.user, category=category).order_by('-added')
    paginator = Paginator(all_routes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'my_profile.html',{'all_routes':page_obj,'categories':categories,
                                             'actual_category':category,'user_info':user_info,
                                             'user_level':user_level, 'category_objects_quantity':category_objects_quantity,
                                             'categories_list':categories_list})

@login_required
def edit_route(request,id,actual_category):
    route = ClimbingRoutes.objects.get(pk=id)
    if request.method == 'POST':
        form = EditRouteForm(request.POST, instance=route)
        if form.is_valid():
            form2=form.save(commit=False)
            form2.user=request.user
            form2.save()
            messages.success(request, 'Your climbing was edited successfully...')
            return HttpResponseRedirect(reverse('my_profile',args=[actual_category]))
        else:
            messages.warning(request, 'Cannot save Your climbing, please check errors below...')
    else:
        form = EditRouteForm(instance=route)
    return render(request,'edit_route.html',{'form':form,'route':route})

@login_required
def delete_route(request,id,actual_category):
    route = ClimbingRoutes.objects.get(pk=id)
    if request.user.id == route.user.id:
        ClimbingRoutes.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('my_profile',args=[actual_category]))

@login_required
def profile_settings(request):
    user_info = get_object_or_404(User,pk=request.user.id)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request,'Profile info saved successfully')
                return HttpResponseRedirect(reverse('profile_settings'))
            else:
                messages.warning(request, 'There were problems with updating your data, please check errors below...')
        else:
            form = UserProfileForm(instance=user_profile)
    except:
        #UserProfile.objects.create(user=request.user)
        user_info = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(instance=user_profile)

    ########### IS USER BEGINEER, SEMI, ADVANCED, PRO ########################
    all_routes = ClimbingRoutes.objects.filter(user=request.user).order_by('-added')
    total_routes = all_routes.count()
    user_level = user_level_counting(total_routes)
    ##########################################################################
    return render(request,'profile_settings.html',{'form':form,'user_info':user_info,'user_level':user_level})

@login_required
def remove_profile_photo(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.photo.delete()
    return HttpResponseRedirect(reverse('profile_settings'))

@login_required
def find_user(request):
    if request.method == 'POST':
        searching_results=[]
        query = request.POST.get('search_user')
        result_list=User.objects.all()
        for item in result_list:
            if (query.upper() in item.username.upper()) or (query.upper() in item.first_name.upper()) or (query.upper() in item.last_name.upper()):
                searching_results.append(item)
    return render(request,'searching_results.html',{'searching_results':searching_results})

@login_required
def searched_profile(request,category,id):
    user=User.objects.get(pk=id)
    all_routes = ClimbingRoutes.objects.filter(user=user).order_by('-added')
    user_info = get_object_or_404(User, pk=id)
    ########### IS USER BEGINEER, SEMI, ADVANCED, PRO ########################
    total_routes=all_routes.count()
    user_level=user_level_counting(total_routes)
    ##########################################################################
    total_likes=user_info.userprofile.total_likes()
    people_liking_profile = user_info.userprofile.likes.all()
    if user_info.userprofile.likes.filter(id=request.user.id).exists():
        can_like='False'
    else:
        can_like='True'
    categories = Category.objects.all()
    if category == 'all':
        return render(request, 'searched_profile.html',{'all_routes': all_routes, 'categories': categories,
                                                        'actual_category': category,'user_info': user_info,
                                                        'total_likes':total_likes,'can_like':can_like,
                                                        'people_liking_profile':people_liking_profile,
                                                        'user_level':user_level})
    all_routes = ClimbingRoutes.objects.filter(user=user, category=category).order_by('-added')
    return render(request, 'searched_profile.html',{'all_routes': all_routes, 'categories': categories,
                                                    'actual_category': category,'user_info': user_info,
                                                    'total_likes':total_likes,'can_like':can_like,
                                                    'people_liking_profile':people_liking_profile,
                                                    'user_level':user_level})

@login_required
def like_profile(request,id):
    if request.method == 'POST':
        liked_user=User.objects.get(pk=id)
        if liked_user.userprofile.likes.filter(id=request.user.id).exists():
            liked_user.userprofile.likes.remove(request.user)
        else:
            liked_user.userprofile.likes.add(request.user)
        liked_user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def route_detail(request,id):
    route=get_object_or_404(ClimbingRoutes,pk=id)
    route_coords=[]
    try:
        route_coords.append(route.location[0])
        route_coords.append(route.location[1])
        is_map=True
    except Exception:
        is_map=False
    return render(request,'route_detail.html',{'route':route_coords,'route_info':route,'is_map':is_map})

def find_route(request):
    found_routes = []
    if request.method == 'POST':
        query=request.POST['find_route']
        searched_routes=ClimbingRoutes.objects.all()
        for result in searched_routes:
            grade=result.official_grade
            if (query.upper() in result.route_name.upper()) or (query == str(grade)):
                found_routes.append(result)
    return render(request,'find_route.html',{'found_routes':found_routes})

def user_level_counting(total_routes):
    if total_routes <= 30:
        user_level = 'Begineer'
    elif total_routes > 30 and total_routes<=60:
        user_level = 'Semi'
    elif total_routes > 60 and total_routes<=100:
        user_level = 'Advanced'
    elif total_routes > 100:
        user_level = 'Pro'
    return user_level