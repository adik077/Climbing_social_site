from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from .models import Category,ClimbingRoutes, RouteGrade
from .views import find_route, all_routes
from django.contrib.auth.models import User

class RoutesTesting(TestCase):
    #### support functions ####
    def creating_route_support(self):
        new_user2 = User.objects.create(username='test', password='Zxcvbnm123')
        category = Category.objects.create(category='test')
        route_grade = RouteGrade.objects.create(category=category, grade='X')
        new_route = ClimbingRoutes.objects.create(user=new_user2, route_name='xyz', category='Mountains',
                                                       area='Tatry', length=100, route_grade_self='5',
                                                       official_grade=route_grade)
        return(new_route)
    ###########################


    #### model testing #####
    def test_adding_category(self):
        new_category = Category.objects.create(category='test')
        self.assertIn(new_category.category,  [category.category for category in Category.objects.all()])

    def test_creating_user(self):
        new_user=User.objects.create(username='test',password='Zxcvbnm123')
        all_users=User.objects.all()
        self.assertEqual(all_users.count(),1)
        self.assertIn(new_user,all_users)

    def test_adding_route(self):
        new_route=self.creating_route_support()
        all_routes=ClimbingRoutes.objects.all()
        self.assertEqual(all_routes.count(),1)
        self.assertIn(new_route,all_routes)


    #### views testing ####
    def test_showing_all_routes(self):
        new_route=self.creating_route_support()
        response=self.client.get('http://127.0.0.1:8000/routes/all/')
        self.assertContains(response,new_route.route_name)

    def test_find_route(self):
        new_route=self.creating_route_support()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['find_route'] = new_route.route_name
        response = find_route(request)
        self.assertIn(new_route.route_name,response.content.decode())


