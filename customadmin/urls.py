from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/apply/<pk>', views.dashboard_apply, name='apply'),
    path('dashboard/apply/<pk>', views.dashboard_apply, name='apply'),
    # description
    path('description/', views.description, name='description'),
    path('adding_Description/', views.add_description, name='add_description'),
    path('description/update/<pk>', views.edit_description, name='update_description'),
    path('description/delete/', views.delete_description, name='delete_description'),
    # testabot
    path('testabot/', views.testabot, name='testabot'),
    # user
    path('user/', views.user, name='user'),
    path('user/edit/<pk>', views.edit_user, name='update_user'),
    path('user/delete/', views.delete_user, name='delete_user'),

    path('signout/', views.signout, name='logout'),
] 

