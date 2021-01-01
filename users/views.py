from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import CustomUser
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import django_tables2 as table
from import_export import resources
from export_download.views import ResourceDownloadMixin
import django_filters
from django.http import HttpResponse



from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm  
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context
from django.views.generic import View
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
user_model = CustomUser


import json
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.views import View

from guardian.conf import settings as guardian_settings
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm, get_objects_for_user

from .tokens import user_tokenizer


class SignUpView(View):
    @staticmethod
    def get(request):
        return render(request, 'signup.html', { 'form': CustomUserCreationForm() })

    @staticmethod
    def post(request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
            message = get_template('acc_active_email.html').render({
              'confirm_url': url
            })
            mail = EmailMessage('Email Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'registration/login.html', {
              'form': AuthenticationForm(),
              'message': f'A confirmation email has been sent to {user.email}. Please confirm to finish registering'
            })

        return render(request, 'signup.html', { 'form': form })
		 
class ConfirmRegistrationView(View):
    @staticmethod
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        
        user = CustomUser.objects.get(pk=user_id)

        context = {
          'form': AuthenticationForm(),
          'message': 'Registration confirmation error . Please click the reset password to generate a new confirmation email.'
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_valid = True
            user.save()
            context['message'] = 'Registration complete. Please login'

        return render(request, 'registration/login.html', context)





class UserDetailView(LoginRequiredMixin, DetailView):
	model = CustomUser
	template_name = 'user_detail.html'
	login_url = 'login'

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = CustomUser
	form_class = CustomUserChangeForm
	template_name = 'user_edit.html'
	success_url = reverse_lazy('article_list')
	login_url = 'login'

	def test_func(self):
		obj = self.get_object()
		return obj.username == self.request.user.username

def search_view(request):
	ctx = {}
	url_parameter = request.GET.get("q")

	if url_parameter:
		users = user_model.objects.filter(username__icontains=url_parameter)
	else:
		users = user_model.objects.all()

	ctx["users"] = users

	if request.is_ajax():
		html = render_to_string(
			template_name="users-results-partial.html", 
			context={"users": users}
		)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)

	return render(request, "users.html", context=ctx)