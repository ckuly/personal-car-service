from django.db import models
import uuid


class CarModel(models.Model):
    """Model representing a car's model."""
    brand = models.CharField('Brand', max_length=100)
    model = models.CharField('Model', max_length=100)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Car(models.Model):
    """Model representing a car."""
    license_plate = models.CharField('License Plate', max_length=6,
                                     help_text='Enter the license plate of a car (example: XXX000)')
    car_model_id = models.ForeignKey('CarModel', on_delete=models.SET_NULL, null=True)
    vin_code = models.CharField('VIN Code', max_length=17, help_text='Enter the VIN code (example: 4Y1SL65848Z411439)')
    client = models.CharField('Client', max_length=100)

    def __str__(self):
        return f"{self.license_plate} ({self.client})"


class Order(models.Model):
    """Model representing a Car Order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID Car Order')
    date = models.DateField('Will be accessible', null=True, blank=True)
    car_id = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)

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

    def __str__(self):
        return f"Order {self.id} for {self.car.license_plate} on {self.date}"


class Service(models.Model):
    """Model representing a car."""
    name = models.CharField('Service Name', max_length=100, help_text='Enter the service provided')
    price = models.DecimalField('Price', max_digits=10, decimal_places=2, help_text='Enter the price of the service')

    def __str__(self):
        return f"{self.name} {self.price}"


class OrderService(models.Model):
    """Model representing a service for a specific order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Service {self.service.name} for Order {self.order.id}"
