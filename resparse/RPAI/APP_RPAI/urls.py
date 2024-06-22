from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parse', views.ResumeParser.as_view(), name='parse'),
]