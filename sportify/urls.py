"""sportify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
import index.views as index
from chat.views import index as chat
from chat.views import receive
from chat.views import user
from index.views import handler404
from index.views import handler500
from index.views import invite_friend
from index.views import accept
from index.views import accept_done
from chat.views import weather
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('invite/', index.invite, name='invite'),
    path('unfriend/<slug:friend_01>/<slug:friend_02>/', index.unfriend, name='unfriend'),
    path('friend_chat/', index.friend_chat, name='friend_chat'),
    path('invite/others/', index.invite_others, name='invite_others'),
    path('chat/', chat, name='chat'),
    path('accept/', accept, name='accept'),
    path('accept/<slug:user_from>/<slug:user_to>/', accept_done, name='accept_done'),
    path('weather/', weather, name='weather'),
    path('user/<int:user_id>/', user, name='user'),
    path('invite/<slug:user_from>/<slug:user_to>/', invite_friend, name='invite_friend'),
    path('receive/<slug:chat_detail>/', receive, name='receive'),
    path('contact/', index.contact,name='contact'),
    path('feedback/', index.feedback,name='feedback'),
    path('successfully_registered/',index.successfully_registered,name='success'),
    path('',index.index,name='home'),
    path('account/', include('accounts.urls')),

    path('basketball/',index.basketball,name='basketball'),
    path('basketball/<slug:date>/',index.basketball_time,name='basketball_time'),
    path('basketball/<slug:date>/<slug:time>/',index.basketball_time_details,name='basketball_time_details'),

    path('cricket/',index.cricket,name='cricket'),
    path('cricket/<slug:date>/',index.cricket_time,name='cricket_time'),
    path('cricket/<slug:date>/<slug:time>/',index.cricket_time_details,name='cricket_time_details'),

    path('football/',index.football,name='football'),
    path('football/<slug:date>/',index.football_time,name='football_time'),
    path('football/<slug:date>/<slug:time>/',index.football_time_details,name='football_time_details'),

    path('badminton/',index.badminton,name='badminton'),
    path('badminton/<slug:date>/',index.badminton_time,name='badminton_time'),
    path('badminton/<slug:date>/<slug:time>/',index.badminton_time_details,name='badminton_time_details'),

    path('chess/',index.chess,name='chess'),
    path('chess/<slug:date>/',index.chess_time,name='chess_time'),
    path('chess/<slug:date>/<slug:time>/',index.chess_time_details,name='chess_time_details'),

    path('table_tennis/',index.table_tennis,name='table_tennis'),
    path('table_tennis/<slug:date>/',index.table_tennis_time,name='table_tennis_time'),
    path('table_tennis/<slug:date>/<slug:time>/',index.table_tennis_time_details,name='table_tennis_time_details'),

    path('snooker/',index.snooker,name='snooker'),
    path('snooker/<slug:date>/',index.snooker_time,name='snooker_time'),
    path('snooker/<slug:date>/<slug:time>/',index.snooker_time_details,name='snooker_time_details'),

    path('volleyball/',index.volleyball,name='volleyball'),
    path('volleyball/<slug:date>/',index.volleyball_time,name='volleyball_time'),
    path('volleyball/<slug:date>/<slug:time>/',index.volleyball_time_details,name='volleyball_time_details'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'sportify'
admin.site.index_title = 'sportify Administration'
admin.site.site_title = 'Admin sportify'


handler404 = handler404
handler500 = handler500
