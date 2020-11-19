from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashPW = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hashPW, confirm_PW = hashPW)
        request.session['loggedInId'] = newUser.id
    return redirect("/travels")

def travels(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "You must logged in first!")
        return redirect("/")
    context = {
        'loggedInUser': User.objects.get(id = request.session['loggedInId']),
        'allTrips' : Trip.objects.all(),
        'favoritedTrips': Trip.objects.filter(joiner=User.objects.get(id = request.session['loggedInId'])),
        'nonfavoritedTrips': Trip.objects.exclude(joiner=User.objects.get(id = request.session['loggedInId']))
    }
    return render(request, "travels.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    errors = User.objects.loginValidator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        userswithSameemail = User.objects.filter(email = request.POST['email'])
        request.session['loggedInId'] = userswithSameemail[0].id
    return redirect("/travels")

def addNewtrip(request):
    return render(request, "newTrip.html")

def newtrip(request):
    print(request.POST)
    errors = Trip.objects.newTripValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/addtrip")
    else:
        createdTrip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], travel_startdate = request.POST['startdate'], travel_enddate = request.POST['enddate'], creator =  User.objects.get(id = request.session['loggedInId']))
        createdTrip.joiner.add(User.objects.get(id=request.session['loggedInId']))
    return redirect("/travels")

def viewTrip(request, tripId):
    context = {
        'Trip' : Trip.objects.get(id=tripId)
    }
    return render(request, "viewTrip.html", context)

def addJoined(request, tripId):
    Trip.objects.get(id=tripId).joiner.add(User.objects.get(id=request.session['loggedInId']))
    return redirect("/travels")

def removeJoined(request, tripId):
    Trip.objects.get(id=tripId).joiner.remove(User.objects.get(id=request.session['loggedInId']))
    return redirect("/travels")

def deleteJoined(request, tripId):
    c = Trip.objects.get(id=tripId)
    c.delete()
    return redirect("/travels")
