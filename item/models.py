from django.db import models


# Create your models here.
class Item(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'предмет'
        verbose_name_plural = 'предмет'

    def __str__(self):
        return self.text[:15]
