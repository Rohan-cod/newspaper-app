from .forms import CustomUserCreationForm
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
from django.contrib.auth.models import User

user_model = CustomUser

class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user_detail.html'
    login_url = 'login'

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
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