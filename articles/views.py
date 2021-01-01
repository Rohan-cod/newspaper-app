from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .forms import ArticleForm
from django.http import JsonResponse
from .models import Article, Comment
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
from .resources import ArticleResource

def export_json(request):
    article_resource = ArticleResource()
    articles = article_resource.export()
    response = HttpResponse(articles.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="articles.json"'
    return response


def export_csv(request):
    article_resource = ArticleResource()
    articles = article_resource.export()
    response = HttpResponse(articles.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="articles.xls"'
    return response

def export_my_csv(request):
    article_resource = ArticleResource()
    queryset = Article.objects.filter(author=request.user)
    my_articles = article_resource.export(queryset)
    response = HttpResponse(my_articles.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="my_articles.xls"'
    return response

def export_my_json(request):
    article_resource = ArticleResource()
    queryset = Article.objects.filter(author=request.user)
    my_articles = article_resource.export(queryset)
    response = HttpResponse(my_articles.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="my_articles.json"'
    return response



@login_required
def home(request):
    return render(request, 'templates/index.html')


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        google_login = user.social_auth.get(provider='google')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'templates/settings.html', {
        'github_login': github_login,
        'google_login': google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        messages.error(request, 'Please correct the error below.')
        
    else:
        form = PasswordForm(request.user)
    return render(request, 'templates/password.html', {'form': form})






class ArticleListView(ResourceDownloadMixin, LoginRequiredMixin, ListView, table.SingleTableMixin):
    model = Article
    template_name = 'article_list.html'
    login_url = 'login'
    paginate_by = 5
    ordering = ['-updated']

class MyArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'my_articles.html'
    login_url = 'login'
    paginate_by = 5
    ordering = ['-updated']
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_new.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'Comment_new.html'
    fields = ('article', 'comment')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentListView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'comment_list.html'
    login_url = 'login'


def search_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        articles = Article.objects.filter(title__icontains=url_parameter)
    else:
        articles = Article.objects.all()

    ctx["articles"] = articles

    if request.is_ajax():
        html = render_to_string(
            template_name="articles-results-partial.html", 
            context={"articles": articles}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "article_search.html", context=ctx)
