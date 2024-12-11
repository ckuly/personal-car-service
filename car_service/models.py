from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


class CarModel(models.Model):
    """Model representing a car's model."""
    brand = models.CharField(_('Brand'), max_length=100, null=False)
    model = models.CharField(_('Model'), max_length=100, null=False)

    class Meta:
        verbose_name = _("Car Model")
        verbose_name_plural = _("Car Models")

    def __str__(self):
        return f"{self.brand} {self.model}"


class Car(models.Model):
    """Model representing a car."""
    license_plate = models.CharField(
        _('License Plate'),
        max_length=6,
        help_text=_('Enter the license plate of a car (example: XXX000)'),
        null=False,
    )
    car_model_id = models.ForeignKey('CarModel', on_delete=models.CASCADE, null=True, verbose_name=_('Car Model'))
    vin_code = models.CharField(
        _('VIN Code'),
        max_length=17,
        help_text=_('Enter the VIN code (example: 4Y1SL65848Z411439)'),
        null=False,
    )
    client = models.CharField(_('Client'), max_length=100, null=False)
    description = HTMLField(_('Description'))
    picture = models.ImageField(_('Picture'), upload_to='pictures', null=True, blank=True)

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def __str__(self):
        return f"{self.license_plate}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)


class Order(models.Model):
    """Model representing a Car Order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('Unique ID Car Order'), null=False)
    date = models.DateField(_('Will be accessible'), null=True)
    car_id = models.ForeignKey('Car', on_delete=models.CASCADE, null=True, verbose_name=_('Car'))
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Client'))

    @property
    def is_overdue(self):
        if self.date and date.today() > self.date:
            return True
        return False

    LOAN_STATUS = (
        ('p', _('Processing')),
        ('d', _('Delivered')),
        ('t', _('Ready To Deliver')),
        ('r', _('Reserved')),
    )

    status = models.CharField(
        _('Status'),
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text=_('Order Status'),
    )

    def car_brand(self):
        return self.car_id.car_model_id.brand

    car_brand.short_description = _('Car Brand')

    def car_model(self):
        return self.car_id.car_model_id.model

    car_model.short_description = _('Car Model')

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.id}"


class Service(models.Model):
    """Model representing a service."""
    name = models.CharField(_('Service Name'), max_length=100, help_text=_('Enter the service provided'), null=False)
    price = models.IntegerField(_('Price'), help_text=_('Enter the price of the service'), null=False)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return f"{self.name}"


class OrderService(models.Model):
    """Model representing a service for a specific order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, verbose_name=_('Order'))
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name=_('Service'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1, null=False)

    class Meta:
        verbose_name = _("Order Service")
        verbose_name_plural = _("Order Services")

    def total_price(self):
        return self.service.price * self.quantity

    total_price.short_description = _('Total Price (EUR)')

    def __str__(self):
        return f"{self.service.name} {self.order.id}"


class OrderReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Order'))
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Reviewer'))
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    content = models.TextField(_('Review'), max_length=2000)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _('Reviews')
        ordering = ['-date_created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    picture = models.ImageField(_('Picture'), default="profile_pics/default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
