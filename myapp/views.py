from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Flight, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.core.mail import send_mail




def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/profile.html')
    else:
        return render(request, 'myapp/signin.html')

def profile_update(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/profile_update.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findflight(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        flight_list = Flight.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if flight_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "Sorry no Flights availiable"
            return render(request, 'myapp/findflight.html', context)
    else:
        return render(request, 'myapp/findflight.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('flight_id')
        seats_r = int(request.POST.get('no_seats'))
        flights = Flight.objects.get(id=id_r)
        if flights:
            if flights.rem > int(seats_r):
                name_r = flights.flight_name
                cost = int(seats_r) * flights.price
                source_r = flights.source
                dest_r = flights.dest
                nos_r = Decimal(flights.nos)
                price_r = flights.price
                date_r = flights.date
                time_r = flights.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = flights.rem - seats_r
                Flight.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, flight_name=name_r,
                                           source=source_r, Flight_id=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                send_mail('AIRSOFT RESERVATION','Your bookin is confirmed','notanesportsorg@gmail.com',[email_r],fail_silently=False,)
                # book.save()
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findflight.html', context)

    else:
        return render(request, 'myapp/findflight.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('flight_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Flight.objects.get(id=book.Flight_id)
            rem_r = bus.rem + book.nos
            Flight.objects.filter(id=book.Flight_id).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that Flight"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findflight.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no Flight booked"
        return render(request, 'myapp/findflight.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r,)
        if user:
            login(request, user)
            return render(request, 'myapp/home.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
