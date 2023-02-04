from django.db import models
class team (models.Model):
        
        img=models.ImageField(upload_to="pics")
        name=models.CharField(max_length=50)
        summ=models.TextField()
class contact(models.Model):
        name=models.CharField(max_length=50)
        email=models.CharField(max_length=100)
        phone=models.CharField(max_length=200)
        address=models.CharField(max_length=400)
class image(models.Model):
        new_img=models.FileField(upload_to="pic" ,max_length=50,null=True )
# Create your models here.
