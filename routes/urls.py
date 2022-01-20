from django.urls import path
from .views import main_dashboard, all_routes, add_route, my_profile,edit_route,delete_route,\
    profile_settings, remove_profile_photo,find_user,searched_profile,like_profile, \
    load_grades,route_detail,find_route

urlpatterns = [
    path('', main_dashboard,name='main_dashboard'),
    path('routes/<str:category>/',all_routes,name='all_routes'),
    path('add_route/',add_route,name='add_route'),
    path('my_profile/<str:category>/',my_profile,name='my_profile'),
    path('edit_route/<int:id>/<str:actual_category>/',edit_route,name='edit_route'),
    path('delete_route/<int:id>/<str:actual_category>/',delete_route,name='delete_route'),
    path('profile_settings/',profile_settings,name='profile_settings'),
    path('remove_profile_photo/',remove_profile_photo,name='remove_profile_photo'),
    path('find_user/',find_user,name='find_user'),
    path('searched_profile/<str:category>/<int:id>/',searched_profile,name='searched_profile'),
    path('like_profile/<int:id>/',like_profile,name='like_profile'),
    path('load_grades',load_grades,name='ajax_load_grades'),
    path('route_detail/<int:id>/',route_detail,name='route_detail'),
    path('find_route/',find_route,name='find_route'),
]
