from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_verification_email(user, request)
            messages.success(request, 'Registration successful. Check your email to verify your account.')
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            # Optional: Redirect based on user role
            if hasattr(user, 'is_employer') and user.is_employer:
                return redirect('employer_dashboard')
            elif hasattr(user, 'is_seeker') and user.is_seeker:
                return redirect('seeker_dashboard')
            else:
                return redirect('home')

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You’ve been logged out.")
    return redirect('login')


def render_home(request):
    return render(request, 'home.html')


def send_verification_email(user, request):
    current_site = get_current_site(request)
    subject = 'Activate your account'
    message = render_to_string('accounts/email_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    user.email_user(subject, message)


def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated!")
        return redirect('home')
    else:
        return render(request, 'accounts/activation_invalid.html')
