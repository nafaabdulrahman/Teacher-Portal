from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:username>/', views.reset_password, name='reset_password'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),

]

# This file defines the URL patterns for the portal app, mapping URLs to views.
# The urlpatterns list routes URLs to views. Each path() function maps a URL pattern to a view function.
