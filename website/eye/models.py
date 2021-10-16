from django.db import models

# Create your models here.
class Performance(models.Model):
	pid=models.IntegerField()
	accuracy=models.FloatField(max_length=100)
	time=models.DateTimeField(max_length=200)
	picture=models.CharField(max_length=100)
	category=models.CharField(max_length=100)

class Patient(models.Model):
	
	Name=models.CharField(max_length=100)
	Number=models.CharField(max_length=100)
	email=models.EmailField(max_length=100)
	password=models.CharField(max_length=100)
	city=models.CharField(max_length=100)
	Dob=models.DateField(max_length=100)
	age=models.CharField(max_length=100)
	Did=models.FloatField(max_length=100)


class Doctor(models.Model):
	Name=models.CharField(max_length=100)
	Number=models.CharField(max_length=100)
	email=models.EmailField(max_length=100)
	password=models.CharField(max_length=100)
	city=models.CharField(max_length=100)
	Dob=models.DateField(max_length=100)
	age=models.CharField(max_length=100)
    
	

