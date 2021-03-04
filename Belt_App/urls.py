from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('user/create', views.create),
    path('results/', views.results),
    path('user/login', views.login),
    path('trip/create', views.new_trip),
    path('trip/<int:id>', views.trip),
    path('logout/', views.logout),
    path('newtrip/', views.newtrippage),
    path('trip/<int:id>/delete', views.delete),
    path('join_trip/<int:id>', views.join_trip),
    path('leave_trip/<int:id>', views.leave_trip)
]	   
