from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import CustomLoginView, CustomRegisterView, ProductListView

urlpatterns =[
    path('', ProductListView.as_view(), name='product-list'),
]

urlpatterns += [
    path('auth/login', CustomLoginView.as_view(), name='login'),
    path('auth/register', CustomRegisterView.as_view(), name='register'),
    path('auth/logout', LogoutView.as_view(), name='logout')
]

