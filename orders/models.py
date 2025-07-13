from django.db import models
from users.models import CustomUser, phone_regex
from books.models import Book


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default=PENDING)

    phone_number = models.CharField(validators=[phone_regex], max_length=13)
    is_paid = models.CharField(default=False)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS):
            raise ValueError('Invalid Error')
        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transition = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
        }
        return new_status in allowed_transition.get(self.status, [])

    def __str__(self):
        return f'{self.user} ordered {self.book}'
