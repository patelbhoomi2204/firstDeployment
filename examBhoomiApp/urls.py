from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('travels', views.travels),
    path('logout', views.logout),
    path('login', views.login),
    path('addtrip', views.addNewtrip),
    path('newtrip', views.newtrip),
    path('view/<int:tripId>', views.viewTrip),
    path('addToJoined/<int:tripId>', views.addJoined),
    path('removeJoined/<int:tripId>', views.removeJoined),
    path('deleteJoined/<int:tripId>', views.deleteJoined),
]