from django.db import models


class Car(models.Model):
    license_plate = models.CharField('License Plate', max_length=6, help_text='Enter the license plate of a car (example: XXX000)')
    car_model_id = models.ForeignKey('Car_model', on_delete=models.SET_NULL, null=True)
    vin_code = models.CharField('VIN Code', max_length=17, help_text='Enter the VIN code (example: 4Y1SL65848Z411439)')
    client = models.CharField('Client', max_length=100)

    def __str__(self):
        return f"{self.license_plate} ({self.client})"