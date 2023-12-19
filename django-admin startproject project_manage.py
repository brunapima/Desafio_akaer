django-admin startproject project_management
cd project_management

python manage.py startapp projects

from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Project(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='projects')

python manage.py makemigrations
python manage.py migrate

from django import forms
from .models import Company, Project

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'members']
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Company, Project
from .forms import CompanyForm, ProjectForm

@login_required
def company_list(request):
    companies = Company.objects.filter(creator=request.user)
    return render(request, 'projects/company_list.html', {'companies': companies})

@login_required
def project_list(request, company_id):
    company = Company.objects.get(id=company_id, creator=request.user)
    projects = Project.objects.filter(company=company)
    return render(request, 'projects/project_list.html', {'company': company, 'projects': projects})

@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.creator = request.user
            company.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'projects/add_company.html', {'form': form})

from django.urls import path
from .views import company_list, project_list, add_company

urlpatterns = [
    path('companies/', company_list, name='company_list'),
    path('companies/add/', add_company, name='add_company'),
    path('companies/<int:company_id>/', project_list, name='project_list'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
]

<!-- companies/company_list.html -->
<h2>Companies</h2>
<ul>
    {% for company in companies %}
        <li><a href="{% url 'project_list' company.id %}">{{ company.name }}</a></li>
    {% endfor %}
</ul>

<!-- projects/project_list.html -->
<h2>{{ company.name }} - Projects</h2>
<ul>
    {% for project in projects %}
        <li>{{ project.name }}</li>
        <ul>
            {% for member in project.members.all %}
                <li>{{ member.username }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
</ul>
<!-- projects/add_company.html -->
<h2>Add Company</h2>
<form method="post" action="{% url 'add_company' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
python manage.py createsuperuser --username=user1 --email=user1@example.com
python manage.py createsuperuser --username=user2 --email=user2@example.com
python manage.py createsuperuser --username=user3 --email=user3@example.com
python manage.py createsuperuser --username=user4 --email=user4@example.com

python manage.py runserver