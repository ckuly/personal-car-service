from django.contrib import admin
from .models import Car, CarModel, Order, Service, OrderService

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'car_id')
    inlines = [OrderServiceInline]

class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'car_model_id', 'vin_code', 'client')
    list_filter = ('client', 'car_model_id')
    search_fields = ('license_plate', 'vin_code')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

admin.site.register(Car, CarAdmin)
admin.site.register(CarModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderService)
