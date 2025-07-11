from django.db import models
from books.models import Book
from users.models import CustomUser


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f'{self.user.username} -> {self.book.title} - {self.rating}'