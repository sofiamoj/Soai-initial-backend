from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


class UserRegisterView(View):
	form_class = UserRegistrationForm
	template_name = 'accounts/register.html'

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			random_code = random.randint(1000, 9999)

			send_mail(
				subject='Welcome to SofiaAI — Your Verification Code',
				message=f"""Hi {form.cleaned_data['full_name']},

Welcome to SofiaAI! ✨

We're excited to have you on board. To complete your
registration, please use the verification code below:

━━━━━━━━━━━━━━━━━━━
Your code:  {random_code}
━━━━━━━━━━━━━━━━━━━

This code expires in 10 minutes.
If you didn't request this, you can safely ignore this email.

Once verified, you'll have access to AI-powered tools,
data analytics insights, and much more.

Best regards,
SofiaAI
AI, Data Science & Web Development""",
				from_email=settings.EMAIL_HOST_USER,
				recipient_list=[form.cleaned_data['email']],
				fail_silently=False,
			)

			OtpCode.objects.update_or_create(
				phone_number=form.cleaned_data['phone'],
				defaults={'code': random_code}
			)
			request.session['user_registration_info'] = {
				'phone_number': form.cleaned_data['phone'],
				'email': form.cleaned_data['email'],
				'full_name': form.cleaned_data['full_name'],
				'password': form.cleaned_data['password'],
			}
			messages.success(request, 'Verification code sent to your email.', 'success')
			return redirect('accounts:verify_code')
		return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
	form_class = VerifyCodeForm

	def get(self, request):
		form = self.form_class()
		return render(request, 'accounts/verify.html', {'form': form})

	def post(self, request):
		user_session = request.session.get('user_registration_info')
		if not user_session:
			messages.error(request, 'Please register first.', 'danger')
			return redirect('accounts:user_register')

		try:
			code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
		except OtpCode.DoesNotExist:
			messages.error(request, 'Code not found. Please register again.', 'danger')
			return redirect('accounts:user_register')

		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			if (timezone.now() - code_instance.created) > timedelta(minutes=10):
				code_instance.delete()
				messages.error(request, 'Code expired. Please register again.', 'danger')
				return redirect('accounts:user_register')

			if cd['code'] == code_instance.code:
				User.objects.create_user(
					user_session['phone_number'],
					user_session['email'],
					user_session['full_name'],
					user_session['password'],
				)
				code_instance.delete()
				del request.session['user_registration_info']
				messages.success(request, 'Registration successful! Welcome.', 'success')
				return redirect('home:home')
			else:
				messages.error(request, 'Incorrect code. Please try again.', 'danger')
				return redirect('accounts:verify_code')

		return render(request, 'accounts/verify.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'You have been logged out successfully.', 'success')
		return redirect('home:home')


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'accounts/login.html'

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			try:
				user_obj = User.objects.get(email=cd['email'])
				user = authenticate(request, phone_number=user_obj.phone_number, password=cd['password'])
			except User.DoesNotExist:
				user = None

			if user is not None:
				login(request, user)
				messages.success(request, 'Welcome back!', 'success')
				return redirect('home:home')
			messages.error(request, 'Email or password is incorrect.', 'warning')
		return render(request, self.template_name, {'form': form})
