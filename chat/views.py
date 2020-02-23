from django.shortcuts import render
from chat.models import *
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests


@login_required
def index(request):

    if request.method == 'POST':
        user = request.user
        chat_detail = request.POST.get('chat_detail')
        message = request.POST.get('message')

        Chat.objects.create(
            user=user, chat_detail=chat_detail, message=message)
        response_data = {}
        response_data['chat_detail'] = chat_detail
        response_data['message'] = message
        response_data['user'] = user.username

        return JsonResponse(response_data)


@login_required
def receive(request, chat_detail):

    obj = Chat.objects.filter(chat_detail=chat_detail).order_by('id')

    response_data = serializers.serialize('json', obj)

    return JsonResponse(response_data, safe=False)


def user(request, user_id):

    user = User.objects.filter(id=user_id)
    response_data = serializers.serialize('json', user)
    return JsonResponse(response_data, safe=False)


def weather(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q=jalandhar&units=metric&appid=f5ce6126037231e34867bae8e05dfc4f'

    city_weather = requests.get(url).json()

    weather = {
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'].title(),
        'icon': city_weather['weather'][0]['icon']
    }
    context = {'weather' : weather}

    return JsonResponse(context, safe=False)
    # return JsonResponse([], safe=False)
