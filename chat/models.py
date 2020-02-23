from django.db import models
from django.core.validators import URLValidator
from django.core.validators import MinLengthValidator
from django.utils.timezone import now
from django.contrib.auth.models import User


class Chat(models.Model):
    class Meta:
        verbose_name_plural = 'Chat'


    user = models.ForeignKey(User,null=True, blank=False, on_delete=models.SET_NULL)
    chat_detail = models.CharField(max_length=30,default='',validators=[MinLengthValidator(4)])
    message = models.CharField(max_length=30,default='',null=True)



    def __str__(self):
        return '{}'.format(self.chat_detail).capitalize()
