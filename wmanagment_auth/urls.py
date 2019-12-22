"""this module contains urls for authentificaton app"""

from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='wmanagment_auth/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]
