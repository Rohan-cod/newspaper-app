from django.urls import path

from .views import SignUpView, UserDetailView, UserUpdateView,  search_view

urlpatterns = [
          
          path('signup/', SignUpView.as_view(), name='signup'),
          path('searc/', search_view, name='search_user'),
    	  path('<int:pk>/',
          UserDetailView.as_view(), name='my_page'),
          path('edit/<int:pk>', UserUpdateView.as_view(), name='user_detail'),

]