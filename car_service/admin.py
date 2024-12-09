from django.contrib import admin
from .models import Car, CarModel, Order, Service, OrderService, OrderReview, Profile


class OrderServiceInline(admin.TabularInline):
    model = OrderService
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'car_id', 'car_brand', 'car_model')
    list_filter = ('date', 'status')
    list_editable = ('date', 'status')
    search_fields = ('id', 'car__model')
    inlines = [OrderServiceInline]

    fieldsets = (
        ('General', {'fields': ('id', 'car_id')}),
        ('Availability', {'fields': ('status', 'date', 'client')}),
    )


class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'car_model_id', 'vin_code', 'client')
    list_filter = ('client', 'car_model_id')
    search_fields = ('license_plate', 'vin_code')
    list_editable = ('client',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price',)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model')
    list_filter = ('brand',)


class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'quantity', 'total_price')
    list_editable = ('service', 'quantity')

class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')

admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderService, OrderServiceAdmin)
admin.site.register(Profile)