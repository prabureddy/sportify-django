from django.shortcuts import render
from django.shortcuts import redirect
from index import forms as formlocal
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, time, timedelta
from datetime import datetime as dt
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from index.models import *
from django.core import serializers
from chat.models import Chat
from django.http import JsonResponse
from django.db.models import Q



def handler404(request,exception):
    return render(request, '404.html', status=404)
def handler500(request):
    return render(request, '500.html', status=500)



@login_required
def unfriend(request,friend_01,friend_02):

    invite1 = Friends.objects.filter(friend_1 = friend_01,friend_2 = friend_02).delete()
    invite2 = Friends.objects.filter(friend_2 = friend_01,friend_1 = friend_02).delete()

    return JsonResponse([],safe=False)


@login_required
def friend_chat(request):

    # Friends.objects.filter(invite_from=user_from, invite_to=user_to)

    # invite1 = Friends.objects.filter(friend_1 = request.user).count()
    # invite2 = Friends.objects.filter(friend_2 = request.user).count()


    obj = Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()

    # if invite1 != 0:
    #     all_user_names.remove(user[0].user)

    response_data = obj

    response_data = serializers.serialize('json', response_data)

    return JsonResponse(response_data,safe=False)



@login_required
def invite_friend(request,user_from,user_to):

    Invite_Friend.objects.get_or_create(invite_from=user_from, invite_to=user_to)

    all_details = {

    }
    return render(request, 'index/index.html', context=all_details)



@login_required
def invite_others(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    login_user = Free.objects.filter(user=request.user)

    all_user = Free.objects.exclude(user=request.user)

    user_dates = login_user[0].free_dates.split(',')

    while("" in user_dates):
        user_dates.remove("")

    count = all_user.count()

    all_user_names = []

    for i in range(0, count):
        all_user_dates = all_user[i].free_dates.split(',')
        while("" in all_user_dates):
            all_user_dates.remove("")

        for a in all_user_dates:
            for b in user_dates:
                if a == b:
                    user = Free.objects.filter(user=all_user[i].user)
                    all_user_names.append(user[0].user)
                    all_user_names = list(dict.fromkeys(all_user_names))

                    invite1 = Invite_Friend.objects.filter(invite_from = request.user, invite_to = all_user[i].user).count()
                    invite2 = Invite_Friend.objects.filter(invite_to = request.user, invite_from = all_user[i].user).count()

                    if invite1 == 1 or invite2 == 1:
                        all_user_names.remove(user[0].user)

        # invite1 = Friends.objects.filter(friend_1 = request.user, friend_2 = all_user[i].user).count()
        # invite2 = Friends.objects.filter(friend_2 = request.user, friend_1 = all_user[i].user).count()
        # if invite1 == 1 or invite2 == 1:
        #     all_user_names.remove(user[0].user)



    # return JsonResponse('hello', safe=False)

    all_details = {
        'all_user': all_user_names,
        # 'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }

    return render(request,'index/invite_others.html',context=all_details)


@login_required
def invite(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Free.objects.all()

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    if request.method == 'POST':
        user = request.user
        check1 = str(request.POST.get('check-1'))
        check2 = str(request.POST.get('check-2'))
        check3 = str(request.POST.get('check-3'))
        check4 = str(request.POST.get('check-4'))
        check5 = str(request.POST.get('check-5'))
        check6 = str(request.POST.get('check-6'))
        check7 = str(request.POST.get('check-7'))

        free_dates = str(check1 + ',' + check2 + ',' + check3 + ',' + check4 + ',' + check5 + ',' + check6 + ',' + check7)

        dup = ''

        free_dates = free_dates.split(',')

        for i in free_dates:
            if i != str(None):
                dup += ','+i

        print(dup)
        if dup == '':
            return redirect('invite')

        Free.objects.filter(user=user).delete()

        Free.objects.create(user=user, free_dates=dup)
        return redirect('invite_others')

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/invite.html', context=all_details)


@login_required
def accept(request):
    invite_to = Invite_Friend.objects.filter(invite_to=request.user)


    # response_data = {}
    response_data = invite_to

    response_data = serializers.serialize('json', response_data)

    return JsonResponse(response_data,safe=False)


@login_required
def accept_done(request,user_from,user_to):

    invite1 = Invite_Friend.objects.filter(invite_from = user_from, invite_to = user_to).delete()
    invite2 = Invite_Friend.objects.filter(invite_from = user_to, invite_to = user_from).delete()

    Friends.objects.get_or_create(friend_1=user_from, friend_2=user_to)

    return JsonResponse('["Done"]',safe=False)


def index(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)

    else:
        upcoming_game = str(0)

    all_details = {
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/index.html', context=all_details)


def contact(request):
    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    contact_form = formlocal.Contactform()
    context = {'form': contact_form, 'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct() }

    if request.method == 'POST':
        contact_form = formlocal.Contactform(request.POST)

        if contact_form.is_valid():
            contact_form.save(commit=True)
            # send message to client
            subject, from_email, to = 'We Received Your Message', 'contact@sportify.com', request.POST.get(
                'email')
            html_content = render_to_string(
                "mail_template/contact_client.html", {'name': request.POST.get('full_name').capitalize()})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            for i in settings.ADMIN_EMAIL:
                # send message to ADMIN
                subject, from_email, to = 'Contacting sportify', 'contact@sportify.com', i
                html_content = render_to_string(
                    "mail_template/contact_admin.html", {'name': request.POST.get('full_name').capitalize()})
                text_content = strip_tags(html_content)
                msg1 = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg1.attach_alternative(html_content, "text/html")
                msg1.send()
            return redirect('/')
        else:
            context = {'form': contact_form, 'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct() }
            return render(request, 'index/contact.html', context=context)
    return render(request, 'index/contact.html', context=context)


def feedback(request):
    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    contact_form = formlocal.Feedbackform()
    context = {'form': contact_form, 'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct() }

    if request.method == 'POST':
        contact_form = formlocal.Feedbackform(request.POST)

        if contact_form.is_valid():
            contact_form.save(commit=True)
            # send message to client
            subject, from_email, to = 'We Received Your Message', 'contact@sportify.com', request.POST.get(
                'email')
            html_content = render_to_string(
                "mail_template/feedback_client.html", {'name': request.POST.get('full_name').capitalize()})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            for i in settings.ADMIN_EMAIL:
                # send message to ADMIN
                subject, from_email, to = 'Contacting sportify', 'contact@sportify.com', i
                html_content = render_to_string(
                    "mail_template/feedback_admin.html", {'name': request.POST.get('full_name').capitalize()})
                text_content = strip_tags(html_content)
                msg1 = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg1.attach_alternative(html_content, "text/html")
                msg1.send()
            return redirect('/')
        else:
            context = {'form': contact_form, 'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct() }
            return render(request, 'index/feedback.html', context=context)
    return render(request, 'index/feedback.html', context=context)


def basketball(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/basketball.html', context=all_details)


def basketball_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/basketball_time.html', context=all_details)


@login_required
def basketball_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Basketball", date=date, time=time).count()
    # print(obj)
    if obj == 10:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/basketball_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/basketball_time_details.html', context=all_details)


def cricket(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/cricket.html', context=all_details)


def cricket_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/cricket_time.html', context=all_details)


@login_required
def cricket_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Cricket", date=date, time=time).count()
    # print(obj)
    if obj == 22:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/cricket_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/cricket_time_details.html', context=all_details)


def football(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/football.html', context=all_details)


def football_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/football_time.html', context=all_details)


@login_required
def football_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Football", date=date, time=time).count()
    # print(obj)
    if obj == 22:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/football_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/football_time_details.html', context=all_details)


def badminton(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/badminton.html', context=all_details)


def badminton_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/badminton_time.html', context=all_details)


@login_required
def badminton_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Badminton", date=date, time=time).count()
    # print(obj)
    if obj == 2:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/badminton_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/badminton_time_details.html', context=all_details)


def chess(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/chess.html', context=all_details)


def chess_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/chess_time.html', context=all_details)


@login_required
def chess_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Chess", date=date, time=time).count()
    # print(obj)
    if obj == 2:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/chess_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/chess_time_details.html', context=all_details)


def table_tennis(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/table_tennis.html', context=all_details)


def table_tennis_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/table_tennis_time.html', context=all_details)


@login_required
def table_tennis_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Table Tennis", date=date, time=time).count()
    # print(obj)
    if obj == 2:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/table_tennis_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/table_tennis_time_details.html', context=all_details)


def snooker(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/snooker.html', context=all_details)


def snooker_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/snooker_time.html', context=all_details)


@login_required
def snooker_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Snooker", date=date, time=time).count()
    # print(obj)
    if obj == 2:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/snooker_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/snooker_time_details.html', context=all_details)


def volleyball(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        date = request.POST.get('date')
        url = date + '/'
        return redirect(url)

    base = dt.today()
    date_list = [base + timedelta(days=x) for x in range(7)]

    all_details = {
        'date': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/volleyball.html', context=all_details)


def volleyball_time(request, date):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        time = request.POST.get('time')
        url = time + '/'
        return redirect(url)

    ds = date
    day, month, year = (int(x) for x in ds.split('-'))
    ans = datetime.date(year, month, day)
    day = ans.strftime("%A")

    base = dt.today()
    date_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    all_details = {
        'selected_date': date,
        'day': day,
        'time': date_list,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/volleyball_time.html', context=all_details)


@login_required
def volleyball_time_details(request, date, time):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    obj = Registered_Players.objects.filter(
        game="Volleyball", date=date, time=time).count()
    # print(obj)
    if obj == 6:
        messages.success(request, 'Slot is filled for selected date ' +
                         date + ' and time ' + time + ' . Try another Slot.')
        all_details = {
            'selected_date': date,
            'selected_time': time,
            'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
        }
        return render(request, 'index/volleyball_time_details.html', context=all_details)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name')
        registration = request.POST.get('registration')
        email = request.POST.get('email')
        game = request.POST.get('game')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Registered_Players.objects.create(user=user, full_name=full_name, registration_no=registration,
                                          email=email, game=game, date=date, time=time)

        subject, from_email, to = 'Registered for Game', 'game@sportify.com', email
        html_content = render_to_string("mail_template/game_registered.html", {'name': request.POST.get('full_name').capitalize(),
                                                                               'game': game, 'date': date, 'time': time, })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')

    all_details = {
        'selected_date': date,
        'selected_time': time,
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/volleyball_time_details.html', context=all_details)


def successfully_registered(request):

    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    all_details = {
        'upcoming_game': upcoming_game,'friend_chat': Friends.objects.filter(Q(friend_1__icontains=request.user) | Q(friend_2__icontains=request.user)).distinct()
    }
    return render(request, 'index/successfully.html', context=all_details)
