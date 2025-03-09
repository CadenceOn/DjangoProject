from django.db import models
from django.contrib.auth.models import User
import json

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принята'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_made')
    animator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests_assigned')
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.customer.username} на {self.event_date}"

class AnimatorOffer(models.Model):
    animator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    available_dates = models.TextField(default='[]', help_text='Список доступных дат в формате JSON (например, ["2025-03-10", "2025-03-11"])')
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='animators/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Объявление от {self.animator.username}"

    def get_available_dates(self):
        return json.loads(self.available_dates) if self.available_dates else []