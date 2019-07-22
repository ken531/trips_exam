from django.shortcuts import render, HttpResponse, redirect
from .models import *
from time import strftime, strptime
from django.contrib import messages

def index(request):
    return render(request, 'trips/index.html')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Please log in', extra_tags='Access denied')
        return redirect ('/')

    user = Users.objects.get(id=request.session['user_id'])
    context = {
        "first_name": user.first_name,
        'alltrips' : trips.objects.all()
    }
    return render(request, 'trips/dashboard.html', context)

def register(request):
    errors = Users.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect('/')
    else:
        request.session['user_id'] = Users.objects.register(request.POST)
        return redirect('/success')

def login(request):
    errors = Users.objects.login(request.POST)
    if errors != None:
        for key, value in errors.items():
            messages.error(request, value,extra_tags=key)
            print(messages)
        return redirect ('/')
    else:
        request.session['user_id'] = Users.objects.get(email=request.POST['email']).id
        return redirect('/success')

def logout(request):
    keys = []
    for key in request.session.keys():
        keys.append(key)
    for key in keys:
        del request.session[key]
    return redirect('/')

def new_trip(request):
    return render(request, 'trips/addnew.html')

def add_new_trip(request):
    errors = trips.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/trips/new')

    else:
        new_trip = trips.objects.create(destination = request.POST['destination'], startdate = request.POST['startdate'], enddate = request.POST['enddate'], plan = request.POST['plan'])
        new_trip_id = new_trip.id
        messages.success(request, 'Trip Successfully added.')
        return redirect (f'/trips/{new_trip_id}')

def display_trip(request, trip_id):
    new_trip = trips.objects.get(id=trip_id)
    context = {
        'trip_html' : new_trip,
    }

    return render(request, 'trips/viewtrip.html', context)

def edit_trip(request, trip_id):
    edittrip = trips.objects.get(id=trip_id)
    context = {
        "trip_html" : edittrip
    }
    messages.success(request, 'Trip successfully updated.')
    return render(request, 'trips/edittrip.html', context)

def process_edit(request, trip_id):
    errors = trips.objects.trip_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f'/trips/{trip_id}/edit')
    else:
        users = trips.objects.get(id=trip_id)
        users.destination = request.POST['destination']
        users.startdate = request.POST['startdate']
        users.enddate = request.POST['enddate']
        users.plan = request.POST['plan']
        users.save()
        return redirect(f'/trips/{trip_id}')

def remove_trip(request, trip_id):
    delete_trip = trips.objects.get(id=trip_id)
    delete_trip.delete()

    return redirect('/success')


