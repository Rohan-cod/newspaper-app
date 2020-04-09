from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserDetailView, UserUpdateView,  search_view, SignUpView, ConfirmRegistrationView

urlpatterns = [

          path('signup/', SignUpView.as_view(), name='signup'),
          path('confirm-email/<str:user_id>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_email'),
          
          path('searc/', search_view, name='search_user'),
    	  path('<int:pk>/',
          UserDetailView.as_view(), name='my_page'),
          path('edit/<int:pk>', UserUpdateView.as_view(), name='user_detail'),

]