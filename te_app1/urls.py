from django.urls import path
from te_app1 import views


urlpatterns = [
    path('<slug:slug>/', views.snippet_detail),
    path('', views.index, name='index'),
    path('output', views.output, name='output'),

]
