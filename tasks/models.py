from django.db import models

# Create your models here.
class Tasks(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    status=models.BooleanField(default=False)
    time_created=models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated=models.DateTimeField(auto_now=True, verbose_name='Время обновления')


    def __str__(self):
        return self.name