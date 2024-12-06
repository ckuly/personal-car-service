from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField

class CarModel(models.Model):
    """Model representing a car's model."""
    brand = models.CharField('Brand', max_length=100, null=False)
    model = models.CharField('Model', max_length=100, null=False)

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"

    def __str__(self):
        return f"{self.brand} {self.model}"


class Car(models.Model):
    """Model representing a car."""
    license_plate = models.CharField('License Plate', max_length=6,
                                     help_text='Enter the license plate of a car (example: XXX000)', null=False)
    car_model_id = models.ForeignKey('CarModel', on_delete=models.CASCADE, null=True)
    vin_code = models.CharField('VIN Code', max_length=17, help_text='Enter the VIN code (example: 4Y1SL65848Z411439)',
                                null=False)
    client = models.CharField('Client', max_length=100, null=False)
    description = HTMLField()

    picture = models.ImageField('Picture', upload_to='pictures', null=True, blank=True)


    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.license_plate}"


class Order(models.Model):
    """Model representing a Car Order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID Car Order', null=False)
    date = models.DateField('Will be accessible', null=True)
    car_id = models.ForeignKey('Car', on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.date and date.today() > self.date:
            return True
        return False

    LOAN_STATUS = (
        ('p', 'Processing'),
        ('d', 'Delivered'),
        ('t', 'Ready To Deliver'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Order Status',
    )

    def car_brand(self):
        return self.car_id.car_model_id.brand

    car_brand.short_description = 'Car Brand'

    def car_model(self):
        return self.car_id.car_model_id.model

    car_model.short_description = 'Car Model'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.id}"


class Service(models.Model):
    """Model representing a service."""
    name = models.CharField('Service Name', max_length=100, help_text='Enter the service provided', null=False)
    price = models.IntegerField('Price', help_text='Enter the price of the service', null=False)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.name}"


class OrderService(models.Model):
    """Model representing a service for a specific order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, null=False)

    class Meta:
        verbose_name = "Order Service"
        verbose_name_plural = "Order Services"

    def total_price(self):
        return self.service.price * self.quantity

    total_price.short_description = 'Total Price (EUR)'

    def __str__(self):
        return f"{self.service.name} {self.order.id}"


class CarReview(models.Model):
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Review', max_length=2000)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = 'Reviews'
        ordering = ['-date_created']