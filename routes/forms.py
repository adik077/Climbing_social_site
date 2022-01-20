from django import forms
from .models import ClimbingRoutes, Category, RouteGrade

class AddRouteForm(forms.ModelForm):
    category = Category.objects.all().values_list('category','category')
    category_list = []
    for item in category:
        category_list.append(item)

    grade = RouteGrade.objects.all().values_list('grade', 'grade')
    grade_list = []
    for item in grade:
        grade_list.append(item)

    route_name = forms.CharField(label="Route name", widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.CharField(label="Category", widget=forms.Select(choices=category_list, attrs={'class':'form-control'}))
    area = forms.CharField(label="Area", widget=forms.TextInput(attrs={'class':'form-control'}))
    length = forms.IntegerField(label="Length", widget=forms.NumberInput(attrs={'class':'form-control'}))
    route_grade_self = forms.CharField(label="Your grade", widget=forms.TextInput(attrs={'class':'form-control'}))
    style = forms.CharField(label="Climbing style",required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    comment = forms.CharField(label="Comment",required=False, widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Write something about this route...'}))

    class Meta:
        model = ClimbingRoutes
        fields = ['route_name','category','area','length','official_grade','route_grade_self','style','comment','location']

        widgets={
            'official_grade':forms.Select(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['official_grade'].queryset = RouteGrade.objects.filter(category=1).order_by('order_number')


        if 'category' in self.data:
            try:
                category_id = self.data.get('category')
                category_id=Category.objects.get(category=category_id)
                category_id=category_id.id
                self.fields['official_grade'].queryset = RouteGrade.objects.filter(category=category_id)
            except (ValueError, TypeError):
                pass
        #elif self.instance.pk:
         #   self.fields['official_grade'].queryset = RouteGrade.objects.filter(self.instance.official_grade)
                #self.instance.category.grades.order_by('grade')


class EditRouteForm(AddRouteForm):

    class Meta:
        model = ClimbingRoutes
        fields = ['route_name','category','area','length','official_grade','route_grade_self','style','comment','location']

        widgets={
            'official_grade':forms.Select(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        actual_category = self.instance.category
        actual_category_id = Category.objects.get(category=actual_category)
        actual_category_id = actual_category_id
        self.fields['official_grade'].queryset = RouteGrade.objects.filter(category=actual_category_id).order_by('order_number')

        if 'category' in self.data:
            try:
                category_id = self.data.get('category')
                category_id = Category.objects.get(category=category_id)
                category_id = category_id.id
                self.fields['official_grade'].queryset = RouteGrade.objects.filter(category=category_id)
            except (ValueError, TypeError):
                pass

