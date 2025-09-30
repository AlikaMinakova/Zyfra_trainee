from django.db import models
from sorl.thumbnail import ImageField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    class Meta:
        abstract = True


class SparePartStatus(models.TextChoices):
    INSTALLED = 'INSTALLED', 'Установлено'
    IN_STOCK = 'IN_STOCK', 'На складе'
    REPAIR = 'REPAIR', 'В ремонте'
    AWAITING_REPAIR = 'AWAITING_REPAIR', 'Ожидает ремонт'


class SparePartLog(models.Model):
    spare_part = models.ForeignKey('SparePart', on_delete=models.CASCADE, related_name='change_logs',
                                   verbose_name='Запчасть')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    message = models.TextField(verbose_name='Комментарий об изменении')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    def __str__(self):
        return f"Изменение для {self.spare_part} от {self.timestamp}"


class SparePartType(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name='Название типа')

    def __str__(self):
        return self.name


class SparePart(TimeStampedModel):
    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE, verbose_name='Тип запчасти')
    vehicle = models.ForeignKey('vehicle.Vehicle', on_delete=models.CASCADE, related_name='spare_parts',
                                verbose_name='Техника')
    status = models.CharField(max_length=20,
                              choices=SparePartStatus.choices,
                              default=SparePartStatus.INSTALLED,
                              verbose_name='Статус'
                              )

    def __str__(self):
        return f"{self.spare_part_type.name} ({self.vehicle})"


class SparePartImage(TimeStampedModel):
    file = ImageField(upload_to='spare_part_images/', verbose_name='Фото')
    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE, related_name='images',
                                        verbose_name='Тип запчасти')


class Attribute(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name='Название атрибута')
    unit = models.CharField(max_length=50, blank=True, verbose_name='Единицы измерения')
    data_type = models.CharField(max_length=50, choices=[
        ('str', 'String'),
        ('int', 'Integer'),
        ('float', 'Float'),
    ], verbose_name='Тип данных')

    def __str__(self):
        return self.name


class AttributeValue(TimeStampedModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Атрибут')
    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE, verbose_name='Тип запчасти')
    value = models.CharField(max_length=255, verbose_name='Значение')
