from django.db import models
from django.core.validators import URLValidator
from django.core.validators import MinLengthValidator
from django.utils.timezone import now
from django.contrib.auth.models import User



class Invite_Friend(models.Model):

    class Meta:
        verbose_name_plural = 'Invite Friend'

    invite_from = models.CharField(max_length=30,default='', blank=True,null=True)
    invite_to = models.CharField(max_length=30,default='', blank=True,null=True)



    def __str__(self):
        return '{} -> {}'.format(self.invite_from,self.invite_to)


class Friends(models.Model):

    class Meta:
        verbose_name_plural = 'Friends'

    friend_1 = models.CharField(max_length=30,default='', blank=True,null=True)
    friend_2 = models.CharField(max_length=30,default='', blank=True,null=True)



    def __str__(self):
        return '{} - {}'.format(self.friend_1,self.friend_2)



class Free(models.Model):
    class Meta:
        verbose_name_plural = 'Free'

    user = models.ForeignKey(User,null=True, blank=False, on_delete=models.SET_NULL)
    free_dates = models.CharField(max_length=30,default='', blank=True,null=True)



    def __str__(self):
        return '{} - Free'.format(self.user).capitalize()




class Contact(models.Model):
    class Meta:
        verbose_name_plural = 'Contact'

    full_name = models.CharField(max_length=30,
                               default='',
                               validators=[MinLengthValidator(4)])
    email = models.EmailField()
    message = models.CharField(max_length=250,
                               default='',
                               blank=False)
    date = models.DateTimeField(default=now, blank=False)



    def __str__(self):
        return '{} contacting'.format(self.full_name).capitalize()




class Feedback(models.Model):
    class Meta:
        verbose_name_plural = 'Feedback'

    full_name = models.CharField(max_length=30,
                               default='',
                               validators=[MinLengthValidator(4)])
    email = models.EmailField()
    message = models.CharField(max_length=250,
                               default='',
                               blank=False)
    date = models.DateTimeField(default=now, blank=False)



    def __str__(self):
        return '{} Feedback'.format(self.full_name).capitalize()


class Registered_Players(models.Model):
    class Meta:
        verbose_name_plural = 'Registered Players'


    user = models.ForeignKey(User,null=True, blank=False, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=30,default='',validators=[MinLengthValidator(4)])
    email = models.EmailField()
    registration_no = models.IntegerField(null=True,blank=True)
    game = models.CharField(max_length=30,default='')
    date = models.CharField(max_length=30,default='')
    time = models.CharField(max_length=30,default='')



    def __str__(self):
        return '{}'.format(self.full_name).capitalize()
