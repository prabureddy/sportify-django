from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from index.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils.html import strip_tags
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse

def index(request):
    return redirect('profile/')


def register(request):
    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.user.is_authenticated:
            return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile = UserProfile.objects.get_or_create(
                user=user,phone_no=profile.phone_no,registration_no=profile.registration_no,passing_year=profile.passing_year
            )

            current_site = get_current_site(request)
            message = render_to_string('mail_template/verify.html', {
                'first_name':user.first_name,
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Sportify account.'
            to_email = form.cleaned_data.get('email')
            text_content = strip_tags(message)
            email = EmailMultiAlternatives(mail_subject, text_content, to=[to_email])
            email.attach_alternative(message, "text/html")
            email.send()
            return render(request, 'account/register.html', {'verify': form,'upcoming_game': upcoming_game,})

    else:
        form = SignupForm()
        profile_form = UserProfileForm()

    return render(request, 'account/register.html', {'form': form,'profile_form':profile_form,'upcoming_game': upcoming_game,})

def activate(request, uidb64, token):
    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/account_activated.html')
    else:
        return render(request, 'account/register.html', {'invalid': 'invalid','upcoming_game': upcoming_game,})



@login_required
def profile(request):
    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    all_details={
        'upcoming_game': upcoming_game,
    }
    return render(request, 'account/profile.html',context=all_details)

class PasswordChangeView(FormView):
    template_name = 'account/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('account:logout')

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your password has been changed Successfully.")
        return super(FormView, self).form_valid(form)

# class ProfileUpdate(UpdateView):
#     # fields ='__all__'
#     fields = ['phone_no','passing_year']
#     template_name = 'account/profile_update.html'
#     success_url = '/'
#
#     def get_object(self):
#         return self.request.user.userprofile


@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        upcoming_game = Registered_Players.objects.filter(user=request.user)
    else:
        upcoming_game = str(0)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(commit=False)
            custom_form.user = user_form
            custom_form.save()
            return redirect(reverse('account:profile'))
        else:
            form = EditProfileForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.userprofile)
            args = {'form': form, 'profile_form':profile_form,'upcoming_game': upcoming_game,}
            return render(request, 'account/profile_update.html', args)
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        args = {'form': form, 'profile_form':profile_form}
        return render(request, 'account/profile_update.html', args)
