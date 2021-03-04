from django.shortcuts import render, HttpResponse, redirect
from .models import Trip, User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def create(request):
    
    if request.method == "POST":

        errors = User.objects.create_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()   

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['new_user'] = new_user.id
        return redirect('/results')

def results(request):
    if 'new_user' not in request.session:
        return redirect('/')

    all_trips = Trip.objects.all()
    context = {
        'confirmed_user': User.objects.get(id=request.session['new_user']),
        'all_trips': all_trips,
            
    }
    return render(request, 'dashboard.html', context)


def login(request):
    if request.method == "POST":

        errors = User.objects.authenticate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        login = User.objects.filter(email=request.POST['email'])
        logged_user = login[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            

            request.session['new_user'] = logged_user.id
            return redirect('/results')


def logout(request):
    request.session.clear()
    return redirect('/')


def new_trip(request):
    if 'new_user' not in request.session:
        return redirect('/')

    if request.method == "POST":

        errors = Trip.objects.trip_manager(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/newtrip/')

        user = User.objects.get(id=request.session['new_user'])
        my_new_trip = Trip.objects.create(
            destination = request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            trip_notes = request.POST['trip_notes'],
            creator = user
        )
        user.added_trips.add(my_new_trip)

        return redirect('/results')


def trip(request, id):
    if 'new_user' not in request.session:
        return redirect('/')

    context = {
        'trip': Trip.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['new_user'])
    }
    return render(request, 'details.html', context)


def newtrippage(request):
    return render(request, 'NewTrip.html')

# def mytrip(request, id):
#     user = User.objects.get(id=request.session['new_user'])
#     trip = Trip.objects.get(id=id)
#     user.added_trips.add(trip)
#     user.save()

#     return redirect(f'/trip/{id}')


def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect('/results')


def join_trip(request, id):
    user = User.objects.get(id=request.session['new_user'])
    trip = Trip.objects.get(id=id)
    user.added_trips.add(trip)
    user.save()

    return redirect('/results')


def leave_trip(request, id):
    user = User.objects.get(id=request.session['new_user'])
    trip = Trip.objects.get(id=id)
    user.added_trips.remove(trip)
    user.save()

    return redirect('/results')

