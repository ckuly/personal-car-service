from django.contrib import admin
from .models import Car, CarModel, Order, Service, OrderService

admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(OrderService)
