from django.db import models
from .models import Book
from django.utils.timezone import now


class FlashSale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        return self.start_time <= now <= self.end_time

    class Meta:
        unique_together = ('product', 'start_time', 'end_time')
