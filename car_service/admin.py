from django.contrib import admin
from .models import Car, CarModel, Order, Service, OrderService


class OrderServiceInline(admin.TabularInline):
    model = OrderService
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'car_id', 'car_brand', 'car_model')
    inlines = [OrderServiceInline]

    def car_brand(self, obj):
        """Returns the Car's Brand"""
        return f"{obj.car_id.car_model_id.brand}"

    car_brand.short_description = 'Car Brand'

    def car_model(self, obj):
        """Returns the Car's Brand"""
        return f"{obj.car_id.car_model_id.model}"

    car_model.short_description = 'Car Model'


class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'car_model_id', 'vin_code', 'client')
    list_filter = ('client', 'car_model_id')
    search_fields = ('license_plate', 'vin_code')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model')
    list_filter = ('brand',)


class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'quantity', 'total_price')

    def total_price(self, obj):
        """Calculate the total price for the service."""
        return obj.service.price * obj.quantity

    total_price.short_description = 'Total Price (EUR)'


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderService, OrderServiceAdmin)
