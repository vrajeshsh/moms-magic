from django.db import models

# Create your models here.

class Kitchen(models.Model):
    kitchen_name = models.CharField(max_length=100)
    kitchen_address = models.CharField(max_length=100)
    kitchen_desc = models.TextField()
    cuisine_type = models.CharField(max_length=100)
    
    def __str__(self):
	    return self.kitchen_name


class Review(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    comment = models.TextField()

    def __str__(self):
	    return self.first_name
