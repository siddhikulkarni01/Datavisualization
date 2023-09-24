from django.db import models

# Create your models here.
class NewUser(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    emailid = models.EmailField()
    phonenumber = models.CharField(max_length=100)
    class Meta:
        db_table = "NewUser"

    def __str__(self):
        return self.firstname