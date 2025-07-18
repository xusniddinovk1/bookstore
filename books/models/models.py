from django.db import models
from django.utils.timezone import now


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_active_flash_sale(self):
        return self.flashsale_set.filter(start_time__lte=now(), end_time__gte=now()).first()

    def get_discounted_price(self):
        flash_sale = self.get_active_flash_sale()
        if flash_sale:
            discount = (self.price * flash_sale.discount_percentage) / 100
            return self.price - discount
        return self.price

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if self.stock < quantity:
            return False

        self.stock -= quantity
        self.save()
        return True

    def increase_stock(self, amount):
        self.stock += amount
        self.save()
        return True

    class Meta:
        ordering = ['title']
