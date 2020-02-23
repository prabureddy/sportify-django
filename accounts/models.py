from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_no = models.BigIntegerField(null=True,blank=True)
    registration_no = models.IntegerField(null=True,blank=True)
    passing_year = models.DateTimeField(blank=False,null=True)

    def clean_registration_no(self):

        registration_no = self.registration_no
        registration_no = len(str(registration_no))

        if registration_no == 8 or registration_no == 5:
            pass
        else:
            raise ValidationError("Enter Correct Registration No.!!!")

        return registration_no

    def clean_phone_no(self):

        phone_no = self.phone_no
        phone_no = len(str(phone_no))

        if phone_no == 10:
            pass
        else:
            raise ValidationError("Enter Correct Mobile No.!!!")

        return phone_no

    def clean_passing_year(self):

        passing_year = self.passing_year
        now = datetime.datetime.now()

        if passing_year > now.year:
            pass
        else:
            raise ValidationError("Enter Correct Passing Year.!!!")

        return passing_year

    def __str__(self):
          return self.user.username
