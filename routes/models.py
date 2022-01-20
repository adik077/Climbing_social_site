from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from mapbox_location_field.models import LocationField

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class RouteGrade(models.Model):
    category = models.ForeignKey(Category, related_name='grades',on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    order_number = models.IntegerField(default=0)

    def __str__(self):
        return self.grade

class ClimbingRoutes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    length = models.IntegerField(validators=[MaxValueValidator(5000),MinValueValidator(1)])
    route_grade_self = models.CharField(max_length=30)
    comment = models.TextField(max_length=300, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    official_grade = models.ForeignKey(RouteGrade, on_delete=models.SET_NULL, null=True)
    style = models.CharField(max_length=30, null=True, blank=True)
    location = LocationField(blank=True,null=True)


    def __str__(self):
        return self.route_name+" | "+self.area

