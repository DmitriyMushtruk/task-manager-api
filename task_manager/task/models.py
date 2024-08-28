from django.db import models


class Task(models.Model):

    TASK_STATUS_CHOICES = (
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    user_id = models.ForeignKey('user.User', to_field='id', on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=300, blank=True)
    status = models.CharField(choices=TASK_STATUS_CHOICES, default='new')

    def __str__(self):
        return self.title
