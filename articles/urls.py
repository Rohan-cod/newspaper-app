from django.urls import path

from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDetailView,
    ArticleDeleteView,
    ArticleCreateView,
    CommentCreateView,
    CommentListView,
)
urlpatterns = [
    path('<int:pk>/edit/',
         ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/',
         ArticleDetailView.as_view(), name='article_detail'), 
    path('<int:pk>/delete/',
         ArticleDeleteView.as_view(), name='article_delete'),
    path('<int:pk>/comment/',
         CommentCreateView.as_view(), name='comment_new'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('comments/<int:pk>/', CommentListView.as_view(), name='comments_list'),
]
