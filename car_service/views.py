from django.http import HttpResponse
from django.shortcuts import render

from .models import CarModel, Car, Order, Service, OrderService


def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders_completed = Order.objects.filter(status__exact='d').count()

    context = {
        'num_cars': num_cars,
        'num_orders_completed': num_orders_completed,
        'num_services': num_services,
    }

    return render(request, 'index.html', context=context)
