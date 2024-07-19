from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    search_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.city}: {self.search_count} раз"
