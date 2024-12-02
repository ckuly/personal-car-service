from django.shortcuts import render, get_object_or_404
from .models import Car, Order, Service
from django.views import generic

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

def cars(request):

    cars = Car.objects.all()
    context = {
        'cars': cars
    }
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})

class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'order_list'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.all().order_by('-date')

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'