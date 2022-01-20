from django.contrib import admin
from .models import ClimbingRoutes, Category,RouteGrade

admin.site.register(Category)

@admin.register(RouteGrade)
class RouteGradeRegister(admin.ModelAdmin):
        list_display = ['category','grade','order_number']
        list_filter = ['category']

@admin.register(ClimbingRoutes)
class ClimbingRoutesRegister(admin.ModelAdmin):
        search_fields = ['user__username','route_name','category','area']
        list_display = ['route_name','category','area','user']
        list_filter = ['added']


