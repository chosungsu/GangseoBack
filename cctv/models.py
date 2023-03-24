from django.db import models

# Create your models here.
class Count(models.Model):
    status = models.CharField(max_length=100)
    counts = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.status}'
class Map(models.Model):
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    summary = models.TextField()
    
    def __str__(self):
        return f'{self.summary}'