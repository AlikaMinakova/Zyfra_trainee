from django.db import models
from sorl.thumbnail import ImageField


class VehicleStatus(models.TextChoices):
    IN_OPERATION = 'IN_OP', 'В работе'
    IDLE = 'IDLE', 'Простой'
    REPAIR = 'REPAIR', 'Ремонт'


class VehicleType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название типа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    reg_number = models.CharField(max_length=20, verbose_name='Регистрационный номер')
    brand = models.CharField(max_length=50, verbose_name='Бренд')
    date_purchase = models.DateField(verbose_name='Дата покупки')
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, verbose_name='Тип техники')
    mileage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Пробег')
    operation_status = models.CharField(
        max_length=20,
        choices=VehicleStatus.choices,
        default=VehicleStatus.IN_OPERATION,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    def __str__(self):
        return f'{self.brand} ({self.reg_number})'


class VehicleImage(models.Model):
    file = ImageField(upload_to='vehicle_images/', verbose_name='Фото')
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Техника'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    def __str__(self):
        return f'Фото для {self.vehicle}'
