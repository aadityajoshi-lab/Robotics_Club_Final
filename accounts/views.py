from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from django.core.mail import send_mail
from .models import EmailVerification
from django.conf import settings

#LOGIN VIEW
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get("remember")
        user = authenticate(request, 
                            username=username,
                              password=password)
        if user:
            login(request, user)
            if remember:
                request.session.set_expiry(60 * 60 * 24 * 14)  # 14 days
            else:
                request.session.set_expiry(0)  # browser close
            messages.success(request, "Login successful!")
            next_url = request.GET.get("next")
            return redirect(next_url or "home")
            
        else:
            messages.error(request, "Invalid username or password")

    else:
        if 'next' in request.GET:
            messages.info(request, "Please login first to access this resource.")
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_check = request.POST.get("passwordCheck")  # <-- get confirm password

        # Check if passwords match
        if password != password_check:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # generate OTP
        otp = random.randint(100000, 999999)
        request.session['reg_otp'] = otp  # make sure session key matches verify_otp

        # store data in session
        request.session['reg_username'] = username
        request.session['reg_email'] = email
        request.session['reg_password'] = password

        # send email
        send_mail(
            subject="Your OTP Verification Code",
            message=f"Your OTP code is {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your email")
        return redirect("verify_otp")

    return render(request, "accounts/register.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("reg_otp")

        if entered_otp and int(entered_otp) == session_otp:
            User.objects.create_user(
                username=request.session['reg_username'],
                email=request.session['reg_email'],
                password=request.session['reg_password']
            )

            # cleanup
            request.session.flush()

            messages.success(request, "Registration successful! You can now login.")
            return redirect("login")

        else:
            messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify_otp.html")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("forgot_password")

        # generate OTP
        otp = random.randint(100000, 999999)

        # store in session
        request.session['reset_otp'] = otp
        request.session['reset_email'] = email

        # send OTP
        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP code is {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your email")
        return redirect("reset_password")

    return render(request, "accounts/forgot_password.html")


def reset_password(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("password")
        password_check = request.POST.get("passwordCheck")
        session_otp = request.session.get("reset_otp")
        email = request.session.get("reset_email")

        if not (entered_otp and session_otp and email):
            messages.error(request, "Session expired. Try again.")
            return redirect("forgot_password")

        if int(entered_otp) != session_otp:
            messages.error(request, "Invalid OTP")
            return redirect("reset_password")

        if new_password != password_check:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        # update password
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # cleanup session
        request.session.flush()

        messages.success(request, "Password updated! You can now login.")
        return redirect("login")

    return render(request, "accounts/reset_password.html")



# LOGOUT VIEW
def user_logout(request):
    logout(request)
    messages.info(request, "Logout Successful!")
    return redirect('home')  
